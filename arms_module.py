#! /usr/bin/env python
import RPi.GPIO as GPIO
import numpy as np
import time
import mcp3008
import irdist
import Tracking
import serial

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Motor Class can be used for any motor function on the rasberry PI.
class Motor:
    __upin = None
    __dpin = None
    __speed = None
    __index = None

    def __init__(self, upin, dpin):
        self.__upin = upin
        self.__dpin = dpin
        GPIO.setup(upin, GPIO.OUT)
        GPIO.setup(dpin, GPIO.OUT)
        return
	#tmove moves the motor in the specified direction for time t.
    def tmove(self, direction, t):
        if (direction == 1):
            GPIO.output(self.__upin, GPIO.HIGH)
            GPIO.output(self.__dpin, GPIO.LOW)
            time.sleep(t)
            self.stop()
        elif(direction == 0):
            GPIO.output(self.__dpin, GPIO.HIGH)
            GPIO.output(self.__upin, GPIO.LOW)
            time.sleep(t)
            self.stop()
        else:
            return

	#move() moves the motor in the specified direction indefinitely.
    def move(self,direction):
        if (direction == 1):
            GPIO.output(self.__upin, GPIO.HIGH)
            GPIO.output(self.__dpin, GPIO.LOW)
        elif (direction == 0):
            GPIO.output(self.__dpin, GPIO.HIGH)
            GPIO.output(self.__upin, GPIO.LOW)
        else:
            return
	#stop() stops all motion on the motor.
    def stop(self):
        GPIO.output(self.__upin, GPIO.LOW)
        GPIO.output(self.__dpin, GPIO.LOW)
        return

class Servo:
    __spin = None
    __freq = None
    __pwm = None
    __neutral = None
    __delay = None

    def __init__(self, spin, freq, neutralduty, delay): #default the freq to 50hz
        self.__spin = spin
        self.__freq = freq
        self.__neutral = neutralduty
        self.__delay = delay
        GPIO.setup(spin, GPIO.OUT)
        self.__pwm = GPIO.PWM(spin, freq) #pin, frequency in hertz
        self.__pwm.start(self.__neutral)
        return

    def servoDefault(self):
        self.__pwm.ChangeDutyCycle(self.__neutral)
        time.sleep(self.__delay)
        return

    def servoMove(self, position):
        self.__pwm.ChangeDutyCycle(position)
        time.sleep(self.__delay)
        return

    def servoStop(self):
        self.__pwm.stop()
        return

class Arm:
    __sArm = None  # abstract servos (1 is the lower one)
    __sClaw = None
    __ser = None

    def __init__(self, s1, s2):
        self.__sArm = s1
        self.__sClaw = s2
        #GPIO.setup(self.__sArm,GPIO.OUT)
        #GPIO.setup(self.__sClaw,GPIO.OUT)
        self.__ser = serial.Serial('/dev/ttyACM0', 9600)
        #self.defaultpos()
        return

    def defaultpos(self):
        #self.__sArm.servoDefault()
        #self.__sClaw.servoDefault()
        return
    
    def armUp(self):
        
        #self.__sArm.servoDefault()
        return
    
    def lungefwd(self):
        #self.__sArm.servoMove(9.5) #change this value later
        #GPIO.output(self.__sArm,True)
        self.__ser.write('l')
        return

    def grab(self):
        #self.__sClaw.servoMove(7)#change this value later
        return

class RWD_Tracks:
    __mR = None
    __mL = None

    def __init__(self, mR, mL):
        self.__mR = mR
        self.__mL = mL
        return

    def forward(self):
        self.stoptracks()
        self.__mR.move(1)#Both Motors move up
        self.__mL.move(1)
        return

    def turnright(self):
        self.stoptracks()
        self.__mR.move(0)
        self.__mR.move(1)
        return

    def turnleft(self):
        self.stoptracks()
        self.__mR.move(1)
        self.__mL.move(0)
        return

    def reverse(self):
        self.stoptracks()
        self.__mR.move(0)#Both Motors move down
        self.__mL.move(0)
        return

    def stoptracks(self):
        self.__mR.stop()
        self.__mL.stop()
        return

class Rover:
    __arm = None
    __tracks = None
    __bluerange = (np.array([110, 50, 100]),np.array([130, 255, 255])) #lower, upper color boundaries, in RGB
    __greenrange = (np.array([24,166,173]),np.array([125,231,236])) #dark green to light green
    __redrange = (np.array([191, 0, 0]),np.array([255, 132, 9]))#dark red to light orange

    __colorList = {1:__bluerange,2:__greenrange,3:__redrange}

    def __init__(self, arm, tracks):
        self.__arm = arm
        self.__tracks = tracks
        return

    def default(self):
        self.__arm.defaultpos()
        return

    def lunge(self):
        self.__arm.lungefwd()
        return

    def seek(self, color):
        '''
            This method seeks a payload with an specific color. It moves the rover
                until it finds the payload.
        :param color: color = {1,2,3}. Color that we want the system to track.
            1 - Blue Range
            2 - Green Range
            3 - Red Range
        :return:
        '''
        colorSelection = self.__colorList[color]  #choose the color from the list
        cvcondition = Tracking.track(colorSelection[0], colorSelection[1]) #getting current state of the target in the frame
        print("Seeking object")
        while (cvcondition == 0):
            self.__tracks.turnright()
            print("Moving Right")
            cvcondition = Tracking.track(colorSelection[0], colorSelection[1])
        self.__tracks.stoptracks()
        print("Found!!!")
        return 

    def center(self, color):
        '''
            This method centers the screen to an specific color payload. It moves the rover
                depending on the position of the payload on the screen.
        :param color: color = {1,2,3}. Color that we want the system to track.
            1 - Blue Range
            2 - Green Range
            3 - Red Range
        :return:
        '''
        colorSelection = self.__colorList[color]  #choose the color from the list
        cvcondition = Tracking.track(colorSelection[0], colorSelection[1]) #getting current state of the target in the frame

        print("Centering")
        while cvcondition != 2: #is going to be trying to center until it is in the middle

            if(cvcondition < 2):#left of center frame
                self.__tracks.turnleft()
                print("Moving left")

            elif(cvcondition > 2):#right of center frame
                self.__tracks.turnright()
                print("Moving Right")

            self.__tracks.stoptracks()
            cvcondition = Tracking.track(colorSelection[0], colorSelection[1])
        print("CENTERED!!!")
        return

    def fwd(self, dist, color):
        glitchfilter = 0
        #While the payload has not yet been detected
        done = False
        oldValue = irdist.get_distance2(4)

        while not done:
            self.__tracks.forward()
            print("moving forward")
            self.center(color)
            value = irdist.get_distance2(4)

            print("new value is {}".format(value))
            print("old value is {}".format(oldValue))

            if abs(value - oldValue) < 10:
                if(value < dist):
                    done = True
                oldValue = value

        self.__tracks.stoptracks()
        return
    
    def findRamp(self, colorToFollow, colorToStop):
        glitchfilter = 0
        #While the payload has not yet been detected
        done = False
        colorSelection = self.__colorList[colorToStop]

        while not done:
            self.__tracks.forward()
            print("moving forward")
            self.center(colorToFollow)

            cvcondition = Tracking.track(colorSelection[0], colorSelection[1])
            if(cvcondition != 0):
                done = True

            
        self.__tracks.stoptracks()
        return

    def navigate(self, dist, color):
        print("here")
        self.seek(color)
        self.center(color)
        self.fwd(dist, color)
        return