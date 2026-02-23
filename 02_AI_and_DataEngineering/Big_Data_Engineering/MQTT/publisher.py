# 3) 

import paho.mqtt.client as mqtt
import time

client = mqtt.Client()

client.connect("localhost", 1883, 60)

ball_number = 1

while True:
    client.publish("/example/1", str(ball_number))
    print("Quarterback has thrown ball number:", ball_number)
    ball_number += 1
    time.sleep(0.5)
