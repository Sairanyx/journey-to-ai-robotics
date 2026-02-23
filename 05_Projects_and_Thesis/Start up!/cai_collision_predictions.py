import cv2
import time
import numpy as np
from ultralytics import YOLO

# ----------------------------
# CONFIG
# ----------------------------
VIDEO_SOURCE = "example.mp4"
MODEL_PATH = "yolov8s.pt"
CONF = 0.35

# COCO classes: person=0, bicycle=1, motorcycle=3 (many e-scooters show up as 3 or 0)
TARGET_CLASSES = {0, 1, 3}

# Draw these polygons for YOUR video frame.
# APPROACH_ROI: where objects approach the crossing (cyclist lane / sidewalk approach)
APPROACH_ROI = np.array([
    [520, 720],
    [980, 720],
    [820, 450],
    [660, 450],
], dtype=np.int32)

# CONFLICT_ZONE: the crossing region (where a collision could occur)
CONFLICT_ZONE = np.array([
    [640, 520],
    [860, 520],
    [920, 640],
    [580, 640],
], dtype=np.int32)

# Collision prediction horizon (seconds) and warning threshold
PREDICT_HORIZON_S = 2.0        # predict 2 seconds ahead
TTC_WARNING_S = 1.5            # warn if predicted entry within 1.5s
MIN_SPEED_PX_PER_S = 120.0     # ignore jitter / stationary objects

# Warning hold
WARNING_HOLD_SECONDS = 1.3


# ----------------------------
# Helpers
# ----------------------------
def point_in_poly(pt, poly):
    return cv2.pointPolygonTest(poly, pt, False) >= 0

def bbox_center_xyxy(xyxy):
    x1, y1, x2, y2 = xyxy
    return (0.5*(x1+x2), 0.5*(y1+y2))

def segment_intersects_polygon(p1, p2, poly):
    """
    Return True if segment p1->p2 intersects polygon edges OR ends inside polygon.
    """
    p1 = tuple(map(float, p1))
    p2 = tuple(map(float, p2))

    # If either point is inside polygon -> intersection
    if point_in_poly(p1, poly) or point_in_poly(p2, poly):
        return True

    # Check against each edge
    for i in range(len(poly)):
        a = tuple(map(float, poly[i]))
        b = tuple(map(float, poly[(i + 1) % len(poly)]))
        if segments_intersect(p1, p2, a, b):
            return True
    return False

def segments_intersect(p1, p2, p3, p4):
    """
    Standard segment intersection test using orientation.
    """
    def orient(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

    def on_segment(a, b, c):
        # c on segment ab
        return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
                min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))

    o1 = orient(p1, p2, p3)
    o2 = orient(p1, p2, p4)
    o3 = orient(p3, p4, p1)
    o4 = orient(p3, p4, p2)

    # General case
    if (o1 * o2 < 0) and (o3 * o4 < 0):
        return True

    # Collinear cases
    eps = 1e-9
    if abs(o1) < eps and on_segment(p1, p2, p3): return True
    if abs(o2) < eps and on_segment(p1, p2, p4): return True
    if abs(o3) < eps and on_segment(p3, p4, p1): return True
    if abs(o4) < eps and on_segment(p3, p4, p2): return True

    return False


# Track state per id: last position + time + smoothed velocity
track_state = {}
warning_until = 0.0


def main():
    global warning_until

    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {VIDEO_SOURCE}")

    model = YOLO(MODEL_PATH)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        t_now = time.time()
        vis = frame.copy()

        # Draw zones
        cv2.polylines(vis, [APPROACH_ROI], True, (255, 255, 255), 2)
        cv2.polylines(vis, [CONFLICT_ZONE], True, (255, 255, 255), 2)
        cv2.putText(vis, "APPROACH", tuple(APPROACH_ROI[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(vis, "CONFLICT", tuple(CONFLICT_ZONE[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        warning_triggered = False
        warning_reasons = []

        results = model.track(
            vis,  # you can pass frame; passing vis is fine too
            persist=True,
            conf=CONF,
            classes=list(TARGET_CLASSES),
            verbose=False,
            tracker="bytetrack.yaml",
        )

        if results and len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            ids = boxes.id

            if ids is not None:
                ids = ids.cpu().numpy().astype(int)
                xyxy = boxes.xyxy.cpu().numpy()
                cls = boxes.cls.cpu().numpy().astype(int)
                confs = boxes.conf.cpu().numpy()

                for i in range(len(xyxy)):
                    track_id = int(ids[i])
                    c = int(cls[i])
                    conf = float(confs[i])

                    cx, cy = bbox_center_xyxy(xyxy[i])
                    center = np.array([cx, cy], dtype=np.float32)

                    inside_approach = point_in_poly((cx, cy), APPROACH_ROI)

                    # Estimate velocity (px/s) with simple smoothing
                    vx, vy = 0.0, 0.0
                    speed = 0.0
                    ttc = None
                    will_intersect = False

                    if track_id in track_state:
                        prev = track_state[track_id]
                        prev_pos = prev["pos"]
                        prev_t = prev["t"]
                        dt = max(1e-3, t_now - prev_t)
                        inst_v = (center - prev_pos) / dt  # px/s vector

                        # EMA smoothing of velocity
                        alpha = 0.35
                        sm_v = alpha * inst_v + (1 - alpha) * prev["v"]
                        vx, vy = float(sm_v[0]), float(sm_v[1])
                        speed = float(np.hypot(vx, vy))

                        # Predict future endpoint after horizon
                        future = center + sm_v * PREDICT_HORIZON_S

                        # Collision prediction: does center->future intersect conflict polygon?
                        if inside_approach and speed >= MIN_SPEED_PX_PER_S:
                            will_intersect = segment_intersects_polygon(center, future, CONFLICT_ZONE)

                            # TTC estimate: approximate time until first entry.
                            # We do a coarse scan along the predicted path.
                            if will_intersect:
                                ttc = estimate_ttc(center, sm_v, CONFLICT_ZONE, max_t=PREDICT_HORIZON_S)

                                if ttc is not None and ttc <= TTC_WARNING_S:
                                    warning_triggered = True
                                    warning_reasons.append(f"id {track_id} TTC={ttc:.2f}s speed={speed:.0f}px/s")

                        # Draw prediction line
                        cv2.line(vis,
                                 (int(cx), int(cy)),
                                 (int(future[0]), int(future[1])),
                                 (255, 255, 255),
                                 2)

                    # Save state
                    track_state[track_id] = {"pos": center, "t": t_now, "v": np.array([vx, vy], dtype=np.float32)}

                    # Draw bbox + label
                    x1, y1, x2, y2 = xyxy[i].astype(int)
                    cv2.rectangle(vis, (x1, y1), (x2, y2), (255, 255, 255), 2)

                    extra = ""
                    if speed > 0:
                        extra = f" v={speed:.0f}"
                    if ttc is not None:
                        extra += f" TTC={ttc:.2f}"
                    if will_intersect:
                        extra += " ->CONFLICT"

                    label = f"id={track_id} cls={c} {conf:.2f}{extra}"
                    cv2.putText(vis, label, (x1, max(25, y1 - 8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Warning hold logic
        if warning_triggered:
            warning_until = max(warning_until, t_now + WARNING_HOLD_SECONDS)

        warning_on = (t_now < warning_until)

        if warning_on:
            cv2.putText(vis, "CAI WARNING: PREDICTED CONFLICT", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
            # Show up to 2 reasons
            for idx, r in enumerate(warning_reasons[:2]):
                cv2.putText(vis, r, (30, 100 + idx * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            # HERE: trigger physical light / relay / GPIO / HTTP
            # trigger_light(True)
        else:
            # trigger_light(False)
            pass

        cv2.imshow("CAI - Collision Prediction", vis)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def estimate_ttc(pos, v, poly, max_t=2.0):
    """
    Coarse TTC estimate: sample along the path and find first time entering polygon.
    pos: (2,) float
    v: (2,) float in px/s
    """
    speed = float(np.hypot(v[0], v[1]))
    if speed < 1e-6:
        return None

    # sample times
    steps = 20
    for k in range(1, steps + 1):
        t = (k / steps) * max_t
        p = pos + v * t
        if point_in_poly((float(p[0]), float(p[1])), poly):
            return t
    return None


if __name__ == "__main__":
    main()