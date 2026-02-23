# 4)

import paho.mqtt.client as mqtt

def receiver_quarterback(client, data, message):
    number = int(message.payload.decode())
    result = number * 2

    client.publish("/example/2", str(result))

    print("Receiver has caught ball number:", number, "Quarterback is throwing ball with number:", result)

client = mqtt.Client()

client.on_message = receiver_quarterback

client.connect("localhost", 1883)
client.subscribe("/example/1")

client.loop_forever()