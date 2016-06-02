import collections, itertools, copy
import numpy, scipy, math, random
import os, sys, time, importlib
import tokenize, re, string
import json, unicodedata
from lib import constants as c

# All variables are being referenced by their index instead of their original
# names.
class vehicle:
    def __init__(self, augArray, compressed=False):
        if not compressed:
            self.vid = augArray[0]
            self.fid = augArray[1]
            self.numFrames = augArray[2]
            self.x = augArray[4]
            self.y = augArray[5]
            self.Vy = augArray[11]
            self.Ay = augArray[12]
            self.Vx = augArray[18]
            self.Ax = augArray[19]
            self.lane = augArray[13]
        else:
            self.vid = augArray[0]
            self.fid = augArray[1]
            self.numFrames = augArray[2]
            self.x = augArray[3]
            self.y = augArray[4]
            self.Vy = augArray[5]
            self.Ay = augArray[6]
            self.Vx = augArray[7]
            self.Ax = augArray[8]

            # self.lane = augArray[13]
            # self.time = augArray[3]
            # self.globalX = augArray[6]
            # self.globalY = augArray[7]
            # self.vLength = augArray[8]
            # self.vWidth = augArray[9]
            # self.vClass = augArray[10]
            # self.precedingVID = augArray[14]
            # self.followingVID = augArray[15]
            self.spaceHeadway = augArray[16]
            self.timeHeadway = augArray[17]

        """
        Uncomment out depending on which model we're running
        This is what you should change to change what's included in the grid.
        """
        self.GridInfo = [1, self.Vx, self.Ax]#, self.spaceHeadway]
        #self.GridInfo = [1, self.Vx, self.Ax]

    
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
    def getGridInfo(self):
        return self.GridInfo
    def getGridInfoLen(self):
        return len(self.GridInfo)
    # def returnCompressedArray(self):
    #     return []
    #     self.vid = augArray[0]
    #     self.fid = augArray[1]
    #     self.numFrames = augArray[2]
    #     self.x = augArray[4]
    #     self.y = augArray[5]
    #     self.Vy = augArray[11]
    #     self.Ay = augArray[12]
    #     self.Vx = augArray[18]
    #     self.Ax = augArray[19]
    #     self.lane = augArray[13]