##
# File: /lib/frame_util.py
# ------------------
# Commonly used functions to load frames/dta
##

import collections, itertools, copy
import scipy, math, random
import numpy as np
import os, sys, time, importlib
import tokenize, re, string
import json, unicodedata
from lib import constants as c

FRAME_TIME = 0.1

def AddVxAx(inFilename, outFilename):
    trajectoryFile = open(inFilename, 'r')
    outFile = open(outFilename, 'w')
    lineNum = 0
    lastVID = 0
    frameCounter = 0
    vidDict = {}
    for line in trajectoryFile.readlines():
        curArray = line.split()
        curVID = int(curArray[0])
        curFrame = int(curArray[1])
        Vx = 0
        Ax = 0
        if lastVID != curVID:
            frameCounter = 0
            vidDict[curVID] = {}
        if frameCounter > 0:
            curY = float(curArray[4])
            preVx = float(vidDict[curVID][curFrame - 1][4])
            Vx = float(curY - preVx)/FRAME_TIME
        if frameCounter > 1:
            curVx = Vx
            prevVx = vidDict[curVID][curFrame - 1][18]
            Ax = (curVx - prevVx)/FRAME_TIME
        curArray.append(Vx)
        curArray.append(Ax)
        vidDict[curVID][curFrame] = curArray
        writeArray = [str(item) for item in curArray]
        writeString = ' '.join(writeArray) + "\n"
        outFile.write(writeString)
        frameCounter += 1
        lastVID = curVID
    trajectoryFile.close()
    outFile.close()
    return vidDict

def VIDToFrameDicts(vidDict):
    frameDict = {}
    vidDictLen = len(vidDict)
    counter = 0
    print(vidDictLen, " entries to convert")
    for elem in vidDict:
        elem = int(elem)
        for vid in vidDict[elem]:
            entry = vidDict[elem][vid]
            curVID = int(entry[0])
            frameID = int(entry[1])
            if frameID not in frameDict:
                frameDict[frameID] = {}
            frameDict[frameID][curVID] = deepcopy(entry)
        if counter % 200 == 0:
            print("Processing.... ", counter, " / ", vidDictLen)
        counter += 1
    return frameDict


def LoadDictFromTxt(filename, dictType):
    trajectoryFile = open(filename, 'r')
    outDict = {}
    for line in trajectoryFile.readlines():
        curArray = np.array(line.split()).astype(float)
        curVID = int(curArray[0])
        curFrame = int(curArray[1])
        if dictType == 'vid':
            if curVID not in outDict:
                outDict[curVID] = {}
            outDict[curVID][curFrame] = curArray
        if dictType == 'frame':
            if curFrame not in outDict:
                outDict[curFrame] = {}
            outDict[curFrame][curVID] = curArray
            
    trajectoryFile.close()
    return outDict