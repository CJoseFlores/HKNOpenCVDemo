# ASME NASA SL
# python trackColor.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time

# 600 by 450 window size


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
#if not args.get("video", False):
 #   camera = cv2.VideoCapture(1)

# otherwise, grab a reference to the video file
#else:
#    camera = cv2.VideoCapture(args["video"])
camera = cv2.VideoCapture(0)

def track(lowerboundary, upperboundary):

    cvcondition = None

    #This variable will be used to tell if either:
    #Any object is in the frame,
    #if the object is too far left from the center
    #if the object is too far right from the center


    # grab the current frane
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        return 0

    #if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        return 0

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    #blurred = cv2.GaussianBlur( frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "blue", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lowerboundary, upperboundary)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    # initialize currentX for x coordinate of center of the object
    currentX = None

    # onlly proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        currentX = (int(M["m10"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # Retrieve width and height of window frame
    width = np.size(frame, 0)
    height = np.size(frame, 0)
    # initialize a and b to be range in center
    # a is 250 and b is 400
    a = (6 * width) / 12
    b = (8 * width) / 12
    # set left and right thresholds to the values
    leftThres = a
    rightThres = b

    # if center of object not in center range
    # print not centered otherwise it is

    if currentX == None:
        return 0

    if currentX < leftThres:
        print("Object is too far left!")
        cvcondition = 1

    elif currentX > rightThres:
        print("Object is too far right!")
        cvcondition = 3
    elif currentX > leftThres and currentX < rightThres:
        print("Object is centered!")
        cvcondition = 2

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    '''
    #if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    '''
    """"
    waitstate = None
    while key == ord("q"):
        waitstate = 0
        print 'waiting'
        while waitstate == 0
            time.sleep(1)
            status = raw_input("Are we still waiting?")
            waitstate = status
            if waitstate != 0
                break
            else:
                continue
        print 'resuming'
        break
    """""

    return cvcondition
