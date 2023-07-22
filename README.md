# SWS3009 Robotics & Deep Learning

## Introduction

National University of Singapore (NUS) School of Computing (SoC) Summer workshop 2023 project repo.

Members (in alphabetical order):

- DENG SIYANG @ BUPT
- LI YIMAN @ SCU
- ZHANG LIXIU @ SCU
- ZHAO XUDA @ SUSTech

Professors:

- Boyd ANDERSON (Robotics)
- Colin TAN (Deep Learning)

## Remote-Control Car for Finding and Recognizing Cats

Baseline model

### Overview

The baseline task is to combine our robot car and our cat recognition deep learing model.

Then use a camera on the robot to discover a room where some photos of 5 categories cats are pasted on any possible objects (such as walls and desk legs), and control the car remotely by our program to recognize which cartegory of the cat we've found.

Besides, we can only see the room details from the camera on the car, without any information about the cats' location, which more sounds like using our car to explore in a first person perspective in a maze.

### Cat Recognition CNN

We use transfer learning to train our cat recognition CNN algorithms applied by our robot from VGG16.

### Robot Control Logic and Hardware Architecture



## Virtual Steering Wheel Car

Advanced model

### Overview

A pretty cool car manipulated by the driver's pose detected from the camera.

Hardware:

- Raspberry Pi 4B
- Pi Camera
- Arduino Mega 2560

Software:

- Python
- MediaPipe Pose Landmark Detection
- Numpy
- OpenCV
- Mosquitto MQTT broker
- Arduino IDE

### Functions

1. Go forward
2. Reverse
3. Turn lert/right
4. Honk
5. Face following
