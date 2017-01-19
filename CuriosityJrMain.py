import RPi.GPIO as GPIO
import time
import os
import numpy as np
import cv2
import argparse
import imutils
from collections import deque
import sys
sys.path.append("Arms/")
import mcp3008
import irdist
from arms_module import *
#sys.path.append("CamTracking/")
import Tracking
#import cvDistance

GPIO.setmode(GPIO.BCM)#Sets the pin Numbering system to GPIO scheme
GPIO.setwarnings(False)

#Enums for Controlling the Motors
U = 1
D = 0
R = U
L = D

#Enums for seek()
blue = 0
green = 1
red = 2

#Enums for fwd()
payloaddist = 25252 #change this value after testing
baydist = 25252 #change this value after testing

#Motor(UpPin,DownPin). Below initializes motor objects
m1 = Motor(21,20)
m2 = Motor(16,12)#
m3 = Motor(26,19)
m4 = Motor(6,13)
#DOWN is close, UP is open
#m1-m4 are motors for the arm
mL = Motor(22,27)     #Left Track
mR = Motor(23,24)     #Right Track

#SClaw = Servo(17,50,10,0.3) #7 is closed and 10 is opened
#SArm = Servo(4,50,8.8,0.3)
SArm = 4;
SClaw = 8;
arm1 = Arm(SArm,SClaw)
tracks = RWD_Tracks(mR,mL)

start = 0 #generic variable that will start the code.

jr = Rover(arm1,tracks)

jr.navigate(9,2)
jr.lunge();
#time.sleep(1)
#jr.claw()
#time.sleep(1)
#jr.up()
#jr.findRamp(2,3)
#jr.navigate(9,3)