import time
import random
import requests
 
API_URL = "http://127.0.0.1:5000/data"

ROBOT_ID = "RB-01"
OBJECTS = ["human", "box", "forklift", "wall"]

while True:
    payload = {
        ROBOT_ID: {
            "measurement_time": int(time.time()),
            "object_class": random.choice(OBJECTS),
            "confidence": round(random.uniform(0.5, 1.0), 2),
            "distance": round(random.uniform(0.2, 10.0), 2)
        }
    }

    r = requests.post(API_URL, json = payload)
    print("Sent", payload)

    time.sleep(1)