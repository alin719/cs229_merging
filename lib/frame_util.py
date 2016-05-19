##
# File: /lib/frame_util.py
# ------------------
# Commonly used functions to load frames/dta
##

import collections, itertools, copy
from copy import deepcopy
import scipy, math, random
import numpy as np
import os, sys, time, importlib
import tokenize, re, string
import json, unicodedata
from lib import constants as c
import matplotlib.pyplot as plt
from IPython import display

FRAME_TIME = 0.1

def AddVxAx(inFilename, outFilename):
    trajectoryFile = open(inFilename, 'r')
    outFile = open(outFilename, 'w')
    lineNum = 0
    lastVID = 0
    frameCounter = 0
    vidDict = {}
    lines = trajectoryFile.readlines()
    numLines = len(lines)
    lineCounter = 0
    for line in lines:
        if lineCounter % 30000 == 0:
            print("Read line ", lineCounter, "/", numLines)
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
        lineCounter += 1
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

#Frame is passed in as a dictionary of vehicles, where
#each vehicle has its full entry in the dict.
def GetGridsFromFrameDict(frameDict):
    gridDict = {}
    for i in frameDict:
        frame = frameDict[i]
        grid = FrameToGrid(frame)
        gridDict[i] = deepcopy(grid)
    return gridDict

def FrameToGrid(frame):
    grid = np.zeros((c.X_DIV + 2, c.Y_DIV + 2, 6))
    for vid in frame:
        vehicleData = frame[vid]
        veh = v.vehicle(vehicleData)
        gridX = int(veh.getX() / c.X_STEP)
        gridY = int(veh.getY() / c.Y_STEP)
        grid[gridX][gridY] = veh.getTrajectory()
    return grid

def GetGridPoints(grid):
    gflat = np.sum(grid, axis=2)
    nz = np.nonzero(gflat)
    nzx = nz[0]*c.X_STEP
    nzy = nz[1]*c.Y_STEP
    return nzx, nzy

def AnimateFrames(frameDict):
    #With a loaded frameDict, animates frames.
    fig_size = plt.rcParams["figure.figsize"]
     
    print("Current size:", fig_size)
     
    # Set figure width to 12 and height to 9
    fig_size[0] = 14
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size
    plt.figure(1)

    for i in range(int(len(frameDict)/2)):
        curFrame = frameDict[100 + i*5]
        plotFrame(curFrame, i)
        plt.clf()

def plotFrame(curFrame, fid):
    x,y = getFramePoints(curFrame)    
    plt.plot(y,70 - x, 'ro')
    plt.title("t = " + str(fid))
    plt.axis([0, 2250, 0, 70])
    display.clear_output(wait=True)
    display.display(plt.gcf())

def getFramePoints(curFrame):
    x = np.array([0]*len(curFrame))
    y = np.array([0]*len(curFrame))
    entryCounter = 0
    for entry in curFrame:
        x[entryCounter] = float(curFrame[entry][4])
        y[entryCounter] = float(curFrame[entry][5])
        entryCounter += 1
    return x,y

