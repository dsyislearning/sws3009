import paho.mqtt.client as mqtt
import numpy as np
import json
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.backend import get_session
from tensorflow.keras.models import Model, load_model
import os.path
import threading

import keyboard

client = None

MODEL_FILE = "cat_recognition_model.h5"

dict = {0:'Persian', 1:'Ragdoll', 2:'Scottish Fold', 3:'Singapura', 4:'Sphynx - Hairless Cat'}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker.")
        client.subscribe("Group_18/IMAGE/classify")
    else:
        print("Connection failed with code: %d" % rc)

def classify_flower(filename, data):
    print("Start classifying")
    result = model.predict(data)
    win = int(np.argmax(result)) # must convert numpy int to python int
    score = float(result[0][win]) # must convert numpy float to python float
    print("Done.")
    return {"filename": filename, "prediction": dict[win], "score": score, "index": win}

def on_message(client, userdata, msg):
    # Payload is in msg. We convert it back to a Python dictionary
    recv_dict = json.loads(msg.payload)
    
    # Recreate the data
    img_data = np.array(recv_dict["data"])
    result = classify_flower(recv_dict["filename"], img_data)

    print("Sending results: ", result)
    client.publish("Group_18/IMAGE/predict", json.dumps(result))

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def send_command(message):
    global client
    client.publish("Group_18/CTRL/move", message)

# 键盘按下事件处理函数
def on_key_press(e):
    if e.name == 'w':
        send_command('w')  # 发送向前的命令
    elif e.name == 's':
        send_command('s')  # 发送向后的命令
    elif e.name == 'a':
        send_command('a')  # 发送向左的命令
    elif e.name == 'd':
        send_command('d')  # 发送向右的命令
    elif e.name == 'g':
        send_command('g')

# 键盘松开事件处理函数
def on_key_release(e):
    print("release")
    send_command('g')  # 发送停止的命令

def main():
    global client
    client = setup("192.168.43.71")
    keyboard.on_press(on_key_press)
    keyboard.on_release(on_key_release)
    while True:
        pass

if __name__ == '__main__':
    if os.path.exists(MODEL_FILE):
        model = load_model(MODEL_FILE)
        print("Successfully loaded model %s" % MODEL_FILE)
        main()
    else: 
        print("There is no such model.")
        exit()

