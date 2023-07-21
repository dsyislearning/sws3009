import surveillance

import signal
import sys
import serial #module for serial port communication
import os

import keyboard

from picamera import PiCamera, Color
#from time import sleep

from threading import Thread
import threading
from time import sleep, ctime
#######################################
#Allow Ctrl-C in case something locks the screen
#######################################
#camera = PiCamera()
camera = surveillance.camera

def emergency(signal, frame):
    print('Something went wrong!')
    sys.exit(0)

# signal.signal(signal.SIGINT, emergency)

#######################################
#Initialization
#######################################
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
judge = 0;

def move_car(input_key):
        ser.write(input_key.encode('utf-8'));
        return input_key

def judge_camera(left, right, head): 
    left_x, left_y = left[0], left[1]
    right_x, right_y = right[0], right[1]
    head_x, head_y = head[0], head[1]

    if(head_x > 640 - 200 or left_x > 640 - 80):
       return 'e'
    elif(head_x < 200 or right_x < 80):
       return 'q'

    return ''

def judge_movement(left, right, head):
    left_x, left_y = left[0], left[1]
    right_x, right_y = right[0], right[1]
    head_x, head_y = head[0], head[1] 
        
    if (abs(left_y - head_y) < 120) or (abs(right_y - head_y) < 120):
        if (left_y > head_y and left_y - right_y > 100):
            return 'a'
        elif (right_y > head_y and right_y - left_y > 100):
            return 'd'
        elif left_y > head_y and right_y > head_y and (abs(right_y - left_y) < 100 and abs(right_x -left_x) < 100):
            return 'l'
        elif left_y > head_y and right_y > head_y and (abs(right_y - left_y) < 100 and abs(right_x - left_x) > 160):
            return 'w'
        elif left_y < head_y and right_y < head_y:
            return 's'
    
    return 'g'

    

#Note: Serial port read/write returns "byte" instead of "str" 
#ser.write("testing serial connection\n".encode('utf-8'))
#ser.write("sending via RPi\n".encode('utf-8'))


