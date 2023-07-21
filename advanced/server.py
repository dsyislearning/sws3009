import paho.mqtt.client as mqtt
import numpy as np
import mediapipe as mp
import cv2

from io import BytesIO
import base64
import json
import os.path
import threading
import time

class BodyPoseDetect:
    def __init__(self, static_image=False, complexity=1, smooth_lm=True, segmentation=False, smooth_sm=True, detect_conf=0.5, track_conf=0.5):
        self.mp_body = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.body = self.mp_body.Pose(static_image, complexity, smooth_lm, segmentation, smooth_sm, detect_conf, track_conf)

    def detect_landmarks(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.body.process(img_rgb)
        detected_landmarks = results.pose_landmarks
        return detected_landmarks

    def get_info(self, detected_landmarks, img_dims):
        lm_list = []
        if not detected_landmarks:
            return False, lm_list

        height, width = img_dims
        for id, b_landmark in enumerate(detected_landmarks.landmark):
            cord_x, cord_y = int(b_landmark.x * width), int(b_landmark.y * height)
            lm_list.append([id, cord_x, cord_y])

        # Find the coordinates of the 15th and 16th landmarks (assuming 0-indexed)
        head = lm_list[0][1:] if len(lm_list) > 0 else None
        left = lm_list[15][1:] if len(lm_list) > 15 else None
        right = lm_list[16][1:] if len(lm_list) > 16 else None

        if left is not None and right is not None and head is not None:
            valid = True
            result = {  "left" : left,
                        "right": right,
                        "head" : head}
            return valid, result
        
        return False, None

client = None

detector = BodyPoseDetect(static_image=True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker.")
        client.subscribe("Group_18/IMAGE/detect")
    else:
        print("Connection failed with code: %d" % rc)

def pose_mp(client, msg):
    recv_dict = json.loads(msg.payload)
    stream = BytesIO(base64.b64decode(recv_dict["data"]))
    original_image = cv2.imdecode(np.frombuffer(stream.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    # t = time.perf_counter()
    image = original_image.copy()
    landmarks = detector.detect_landmarks(image)
    valid, result = detector.get_info(landmarks, image.shape[:2])
    # print(f'cost:{time.perf_counter() - t:.8f}s')
    print(valid)
    if valid == True:
        client.publish("Group_18/CTRL/move", json.dumps(result))
        log_debug("Send result " + str(result))
    elif valid == False:
        client.publish("Group_18/CTRL/signal", 'g')

def on_message(client, userdata, msg):
    if msg.topic == "Group_18/IMAGE/detect":
        pose_mp(client, msg)

def setup(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(hostname)
    client.loop_start()
    return client

def main():
    global client
    client = setup("192.168.43.71")
    while True:
        pass

if __name__ == '__main__':
    main()
