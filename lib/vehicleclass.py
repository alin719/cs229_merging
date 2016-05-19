import collections, itertools, copy
import numpy, scipy, math, random
import os, sys, time, importlib
import tokenize, re, string
import json, unicodedata
import lib.constants as c
from lib import constants as c

# All variables are being referenced by their index instead of their original
# names.
class vehicle:
    def __init__(self, augArray):
        self.vid = augArray[0]
        self.fid = augArray[1]
        self.numFrames = augArray[2]
        self.time = augArray[3]
        self.x = augArray[4]
        self.y = augArray[5]
        self.globalX = augArray[6]
        self.globalY = augArray[7]
        self.vLength = augArray[8]
        self.vWidth = augArray[9]
        self.vClass = augArray[10]
        self.Vy = augArray[11]
        self.Ay = augArray[12]
        self.lane = augArray[13]
        self.precedingVID = augArray[14]
        self.followingVID = augArray[15]
        self.spaceHeadway = augArray[16]
        self.timeHeadway = augArray[17]
        self.Vx = augArray[18]
        self.Ax = augArray[19]
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getFrame(self):
        return self.fid
    def getVx(self):
        return self.Vx
    def getAx(self):
        return self.Ax
    def getVy(self):
        return self.Vy
    def getAy(self):
        return self.Vy
    def getTrajectory(self):
        return [self.x, self.y, self.Vx, self.Vy, self.Ax, self.Ay]