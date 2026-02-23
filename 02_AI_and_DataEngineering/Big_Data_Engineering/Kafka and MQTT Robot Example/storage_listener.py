import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "incoming_data"

OUTPUT_FILE = "robot_events.jsonl"

def on_message(client, userdata, message):

    text = message.payload.decode("utf-8")

    file = open(OUTPUT_FILE, "a")
    file.write(text + "\n")
    file.close()

    print("Saved this:", text)

client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT)
client.subscribe(MQTT_TOPIC)

print("Listening for", MQTT_TOPIC, "!")

client.loop_forever()