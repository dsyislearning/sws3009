

import signal
import sys
import serial #module for serial port communication
import os

import keyboard

from picamera import PiCamera, Color
#from time import sleep
import time

from threading import Thread
import threading
from time import sleep, ctime
#######################################
#Allow Ctrl-C in case something locks the screen
#######################################
camera = PiCamera()

def emergency(signal, frame):
    print('Something went wrong!')
    sys.exit(0)

signal.signal(signal.SIGINT, emergency)

#######################################
#Initialization
#######################################
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
judge = 0;
from datetime import datetime

def open_screen():
    camera.start_preview(window=(0, 0, 1080, 1080), fullscreen=False)
    

def open_full_screen():
    camera.start_preview(fullscreen=True)
    
def close_screen():
    camera.stop_preview()

def get_image():
        filename = datetime.now().strftime("%Y%m%d-%H%M%S" + ".jpg")
        camera.capture("./samples/" + filename)
        return filename

def move_car(input_key):
        ser.write(input_key.encode('utf-8'));
        return input_key
             



#Note: Serial port read/write returns "byte" instead of "str" 
#ser.write("testing serial connection\n".encode('utf-8'))
#ser.write("sending via RPi\n".encode('utf-8'))


