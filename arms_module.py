#! /usr/bin/env python
import numpy as np
import time
import Tracking

class Rover:
    __arm = None
    __tracks = None
    __bluerange = (np.array([110, 50, 100]),np.array([130, 255, 255])) #lower, upper color boundaries, in RGB
    __greenrange = (np.array([24,166,173]),np.array([125,231,236])) #dark green to light green
    __redrange = (np.array([191, 0, 0]),np.array([255, 132, 9]))#dark red to light orange

    __colorList = {1:__bluerange,2:__greenrange,3:__redrange}

    def __init__(self):
		# Do Nothing
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
            print("Moving Right")
            cvcondition = Tracking.track(colorSelection[0], colorSelection[1])
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
                print("Moving left")

            elif(cvcondition > 2):#right of center frame
                print("Moving Right")

            cvcondition = Tracking.track(colorSelection[0], colorSelection[1])
        print("CENTERED!!!")
        return

    def fwd(self, dist, color):
        glitchfilter = 0
        #While the payload has not yet been detected
        done = False
        oldValue = 200; # Added this to not need an IR Sensor.

        while not done:
            print("moving forward")
            self.center(color)
            value = 200; # Added this value to not need an IR Sensor.

            print("new value is {}".format(value))
            print("old value is {}".format(oldValue))

            if abs(value - oldValue) < 10:
                if(value < dist):
                    done = True
                oldValue = value
        return
    
    def findRamp(self, colorToFollow, colorToStop):
        glitchfilter = 0
        #While the payload has not yet been detected
        done = False
        colorSelection = self.__colorList[colorToStop]

        while not done:
            print("moving forward")
            self.center(colorToFollow)

            cvcondition = Tracking.track(colorSelection[0], colorSelection[1])
            if(cvcondition != 0):
                done = True
        return

    def navigate(self, dist, color):
        print("here")
        self.seek(color)
        self.center(color)
        self.fwd(dist, color)
        return
