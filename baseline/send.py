import control

import paho.mqtt.client as mqtt
import numpy as np
from PIL import Image
import json
from os import listdir
from os.path import join

SAMPLE_PATH = "./samples"

LEN = 224

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected.")
        client.subscribe("Group_18/IMAGE/predict")
        client.subscribe("Group_18/CTRL/move")
    else:
        print("Failed to connect. Error code: %d" % rc)

def on_message(client, userdata, msg):
    if msg.topic == 'Group_18/IMAGE/predict':
        # print("Received message from server.")
        resp_dic = json.loads(msg.payload)
        print("Filename: %s, Prediction: %s, Score: %3.4f" % (resp_dic["filename"], resp_dic["prediction"], float(resp_dic["score"])))
    elif msg.topic == 'Group_18/CTRL/move':
        move_car(str(msg.payload.decode('utf-8')))

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def load_imge(filename):
    img = Image.open(filename)
    img = img.resize((LEN, LEN))
    imgarray = np.array(img) 
    final = np.expand_dims(imgarray, axis = 0)
    return final

def send_image(client, filename):
    img = load_imge(filename)
    img_list = img.tolist()
    send_dict = {"filename": filename, "data": img_list}
    client.publish("Group_18/IMAGE/classify", json.dumps(send_dict))

def main():
    client = setup("127.0.0.1")
    # print("Waiting for keyboard input.")
    while True:
        pass

# In this manner, the Python file's code inside the if condition is only run
if __name__ == '__main__':
    main()
