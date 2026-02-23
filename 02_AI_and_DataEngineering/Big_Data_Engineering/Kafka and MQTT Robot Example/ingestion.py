# Did the same thing for the temperature but for the scenario asked in q 2 and 3


from flask import Flask, request, jsonify
import time
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)

KNOWN_ROBOTS = {"RB-01"}

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "incoming_data"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT)

def validation(data):

    if not isinstance(data, dict):
        return False, "Data must be a JSON object"
    
    if len(data) != 1:
        return False, "Must containe only one robot_id"
    
    robot_id = list(data.keys())[0]

    if robot_id not in KNOWN_ROBOTS:
        return False, "Uknown robot detected!"
    
    values_data = data[robot_id]

    if "measurement_time" not in values_data:
        return False, "Missing the measurement_time"
    if "object_class" not in values_data:
        return False, "Missing the object_class"
    if "confidence" not in values_data:
        return False, "Missing the confidence"
    if "distance" not in values_data:
        return False, "Missing the distance"

    if not isinstance(values_data["measurement_time"], int):
        return False, "The measurement_time has to be an integer"

    if values_data["measurement_time"] > int(time.time()) + 20:
        return False, "The measurement_time can't be in the future"

    if not isinstance(values_data["object_class"], str):
        return False, "The object_class has to be a string"

    if not isinstance(values_data["confidence"], (int, float)):
        return False, "The confidence has to be a number"

    if values_data["confidence"] < 0 or values_data["confidence"] > 1:
        return False, "The confidence has be between 0 and 1"

    if not isinstance(values_data["distance"], (int, float)):
        return False, "The distance has to be a number"

    if values_data["distance"] < 0:
        return False, "The distance has to be positive"

    return True, "The robot is sending valid data!"

@app.route("/data", methods = ["POST"])

def ingest():

    data = request.get_json()

    if data is None:
        return jsonify({"Error": "No Json was received from Robot"})

    answer, message = validation(data)

    if not answer:
        return jsonify({"Error": message})

    mqtt_client.publish(MQTT_TOPIC, json.dumps(data))

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000)
    

    

