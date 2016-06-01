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
from lib import vehicleclass as v

FRAME_TIME = 0.1

"""
Function: AddVxAx:
Essentially used once to initialize the Vy and Ay values

"""
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

"""
Function: VIDToFrameDicts:
Converts a dictionary based on VID keys to a dictionary based
on FrameID keys.

"""

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

"""
Function: LoadDictFromTxt
Params: filename, dictType

Takes a full-path filename of an entry file and loads the info into memory
as a dictionary.  The dictType param determines whether the returned dictionary
is keyed by frameID or VID
"""

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

"""
Function: GetGridsFromFrameDict

Takes a dictionary based on frameIDs, converts to a dictionary
of grids based on frameID.  Calls FrameToGrid, which does most
of the work

"""

#each vehicle has its full entry in the dict.
def GetGridsFromFrameDict(frameDict):
    gridDict = {}
    for i in frameDict:
        frame = frameDict[i]
        grid = FrameToGrid(frame)
        gridDict[i] = deepcopy(grid)
    return gridDict

"""
Function: GetGridIndices

Takes in an x and a y, and returns the indies in the currently dimensioned
grid.

"""

def GetGridIndices(givenX, givenY):
    gridX = int((givenX - c.MIN_GRID_X) / c.X_STEP)
    gridY = int((givenY - c.MIN_GRID_Y) / c.Y_STEP)
    return gridX, gridY


"""
Function: MeanCenterGrid

Takes in a grid, and subtracts the mean of all values besides #vehicles.

"""

def MeanCenterGrid(grid):
    x, y, z = grid.shape
    means = np.zeros(z)
    for i in range(x):
        for j in range(y):
            numVehicles = grid[i][j][0]
            scaledVals = grid[i][j]*numVehicles
            scaledVals[0] = numVehicles
            means += scaledVals
    means /= means[0]
    means[0] = 0
    for i in range(x):
        for j in range(j):
            grid[i][j] -= means
    return grid

    

"""
Function: FrameToGrid

Converts info from a frame (dict of VIDs for all cars in a particular
frame) into a grid populated with entries if a vehicle is present at
that location.

"""

def FrameToGrid(frame):
    #Creates grid determined by DIV numbers in constants.py
    grid = np.zeros((c.X_DIV, c.Y_DIV, 3)) # is number of elems in trajectory info
    for vid in frame:
        vehicleData = frame[vid]
        veh = v.vehicle(vehicleData)
        if not InGridBounds(veh.getX(), veh.getY()):
            continue
        # Scales the grid into the desired window - check constants.py
        # to edit MIN/MAX_GRID values.
        gridX, griDY = GetGridIndices(veh.getX(), veh.getY())
        grid[gridX][gridY] += veh.getGridInfo()
        grid = MeanCenterGrid(grid)
    return grid

"""
Function: InGridBounds

Checks if a given x and y are within the constant bounds
of the desired grid.  Returns True if true, False if false.

"""

def InGridBounds(givenX, givenY):
    if givenX < c.MIN_GRID_X or givenX > c.MAX_GRID_X:
        return False
    if givenY < c.MIN_GRID_Y or givenY > c.MAX_GRID_Y:
        return False
    return True

"""
Function: GetGridPoints

This is basically just used for animation, but tests a given grid
for nonzero indices, then calculates their positions in the original
frame (does not decompress), for display purposes

"""

def GetGridPoints(grid):
    gflat = np.sum(grid, axis=2)
    nz = np.nonzero(gflat)
    nzx = nz[0]*c.X_STEP
    nzy = nz[1]*c.Y_STEP
    return nzx, nzy

"""
Function: Animate Frames

Given a dictionary and an input type, animates the dictionary in time order

"""

def AnimateFrames(inputDict, inputType='frame'):
    #With a loaded frameDict, animates frames.
    fig_size = plt.rcParams["figure.figsize"]
     
    print("Current size:", fig_size)
     
    # Set figure width to 12 and height to 9
    fig_size[0] = 14
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size
    plt.figure(1)

    for i in range(int(len(inputDict)/2)):
        curFrame = inputDict[100 + i*5]
        if inputType == 'frame':
            plotFrame(curFrame, i)
        if inputType == 'grid':
            plotGrid(curFrame, i)
        plt.clf()

"""
Function: plotFrame

Helper to plot a given frame

"""
def plotFrame(curFrame, fid):
    x,y = getFramePoints(curFrame)    
    plt.plot(y,70 - x, 'ro')
    plt.title("t = " + str(fid))
    plt.axis([0, 2250, 0, 70])
    display.clear_output(wait=True)
    display.display(plt.gcf())

"""
Function: plotGrid

Helper to plot a given grid

"""

def plotGrid(curGrid, fid):
    gflat = np.sum(curGrid, axis=2)
    nz = np.nonzero(gflat)
    nzx = nz[0]*c.X_STEP
    nzy = nz[1]*c.Y_STEP
    plt.title("t = " + str(fid))
    plt.axis([0, 2250, -70, 0])
    plt.plot(nzy, -nzx, 'ro')
    display.clear_output(wait=True)
    display.display(plt.gcf())

"""
Function: getFramePoints

Plots a given 

"""
def getFramePoints(curFrame):
    x = np.array([0]*len(curFrame))
    y = np.array([0]*len(curFrame))
    entryCounter = 0
    for entry in curFrame:
        x[entryCounter] = float(curFrame[entry][4])
        y[entryCounter] = float(curFrame[entry][5])
        entryCounter += 1
    return x,y

