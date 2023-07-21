import control
import surveillance

import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
import json
from os import listdir
from os.path import join
from io import BytesIO
from datetime import datetime
import base64
import time

LEN = 224

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected.")
        client.subscribe("Group_18/#")
    else:
        print("Failed to connect. Error code: %d" % rc)

def on_message(client, userdata, msg):
    if msg.topic == "Group_18/IMAGE/test":
        send_image(client)
        print(msg.payload.decode('utf-8'))
    elif msg.topic == "Group_18/CTRL/move":
        recv_dict = json.loads(msg.payload)
        left = recv_dict["left"]
        right = recv_dict["right"]
        head = recv_dict["head"]
        signal = control.judge_movement(left, right, head)
        signal += control.judge_camera(left, right, head)
        print("Signal: " + str(signal))
        print("left: ", left)
        print("right:", right)
        print("head: ", head)
        control.move_car(signal)
    elif msg.topic == "Group_18/CTRL/signal":
        control.move_car(msg.payload.decode('utf-8'))
        print("No driver!")

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def send_image(client):
    filename = datetime.now().strftime("%Y%m%d-%H%M%S" + ".jpg")
    stream = BytesIO()
    #surveillance.camera.capture(join("./samples", filename))
    surveillance.camera.capture(stream, format="jpeg")
    data = base64.b64encode(stream.getvalue()).decode('utf-8')
    send_dict = {"filename": filename, "data": data}
    client.publish("Group_18/IMAGE/detect", json.dumps(send_dict))
    time.sleep(0.05)

def main():
    client = setup("127.0.0.1")
    while True:
        send_image(client)

# In this manner, the Python file's code inside the if condition is only run
if __name__ == '__main__':
    main()
