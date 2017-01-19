import time
import os
import numpy as np
import cv2
import argparse
import imutils
from collections import deque
import sys
from arms_module import *
import Tracking


demo = Rover()

demo.navigate(9,2) # 9 is the distance, 2 is the color.

