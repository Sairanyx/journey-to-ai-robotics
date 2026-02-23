import cv2
import time
import numpy as np
from ultralytics import YOLO

# ----------------------------
# CONFIG (tune these)
# ----------------------------
VIDEO_SOURCE = 0  # 0 for webcam, or "video.mp4"
MODEL_PATH = "yolov8s.pt"  # try yolov8n.pt if slow
CONF = 0.35

# Classes (COCO): person=0, bicycle=1, motorcycle=3
TARGET_CLASSES = {0, 1, 3}

# "Approach corridor" polygon in image pixels (edit by clicking points if you want later)
# Example: a trapezoid region where cyclists approach the crossing
ROI_POLY = np.array([
    [500, 720],
    [900, 720],
    [760, 420],
    [640, 420],
], dtype=np.int32)

# Speed threshold (pixel/s). Start here; tune after you see values.
SPEED_THRESHOLD_PX_PER_S = 250.0

# If you want warning to stay on for a minimum time
WARNING_HOLD_SECONDS = 1.5


# ----------------------------
# Helpers
# ----------------------------
def point_in_poly(pt, poly):
    # pt: (x,y)
    return cv2.pointPolygonTest(poly, pt, False) >= 0

def bbox_center_xyxy(xyxy):
    x1, y1, x2, y2 = xyxy
    return (0.5*(x1+x2), 0.5*(y1+y2))

# Track state: last position + time per track_id
track_state = {}
warning_until = 0.0


def main():
    global warning_until

    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {VIDEO_SOURCE}")

    model = YOLO(MODEL_PATH)

    # Use Ultralytics tracking (ByteTrack default). persist=True keeps IDs stable across frames.
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        t_now = time.time()

        # Track on this frame
        results = model.track(
            frame,
            persist=True,
            conf=CONF,
            classes=list(TARGET_CLASSES),
            verbose=False,
            tracker="bytetrack.yaml",
        )

        vis = frame.copy()

        # Draw ROI
        cv2.polylines(vis, [ROI_POLY], isClosed=True, color=(255, 255, 255), thickness=2)

        warning_triggered = False

        if results and len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes

            # boxes.id exists when tracking is active
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

                    # Only consider if center point inside ROI
                    inside = point_in_poly((cx, cy), ROI_POLY)

                    # Speed estimate (pixel/s)
                    speed = 0.0
                    if track_id in track_state:
                        (px, py, pt) = track_state[track_id]
                        dt = max(1e-3, (t_now - pt))
                        dist = np.hypot(cx - px, cy - py)
                        speed = dist / dt

                    track_state[track_id] = (cx, cy, t_now)

                    # Trigger logic
                    if inside and speed >= SPEED_THRESHOLD_PX_PER_S:
                        warning_triggered = True

                    # Draw box + label
                    x1, y1, x2, y2 = xyxy[i].astype(int)
                    cv2.rectangle(vis, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    label = f"id={track_id} cls={c} {conf:.2f} v={speed:.0f}px/s"
                    cv2.putText(vis, label, (x1, max(25, y1 - 8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Warning hold logic
        if warning_triggered:
            warning_until = max(warning_until, t_now + WARNING_HOLD_SECONDS)

        warning_on = (t_now < warning_until)

        if warning_on:
            cv2.putText(vis, "WARNING: FAST APPROACH", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            # Here is where you'd trigger your physical light:
            # trigger_light(True)
        else:
            # trigger_light(False)
            pass

        cv2.imshow("CAI - detect/track/warn", vis)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()