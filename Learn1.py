# -*- coding: utf-8 -*-
"""
Created on Thu May 19 10:49:48 2016

@author: Derek
"""

from lib import frame_util as futil
from lib import util
from sklearn import linear_model
import numpy as np
import os
from scipy import sparse
from lib import constants

VID = 1-1
FID = 2-1
TOTFS = 3-1
GlobalT = 4-1
LocalX = 5-1
LocalY = 6-1
GlobalX = 7-1
GlobalY = 8-1
Len = 9-1
Wid = 10-1
Class = 11-1
Vel = 12-1
Accel = 13-1
LaneID = 14-1
Preceding = 15-1
Following = 16-1
Spacing = 17-1
Headway = 18-1


numUsing = 10
#def getStartVals(ID, dictd):
    
#get the training examples
def getX(filename):
    #filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
    path = os.getcwd()+'/'
    frameDict = futil.LoadDictFromTxt(path+filename, 'frame')
    dictOfGrids = futil.GetGridsFromFrameDict(frameDict)
    a = len('aug_trajectories-0750am-0805am.txt')
    MR = np.loadtxt(path+filename[:-a]+'mergeTrajectoryInfo/'+filename[(-a+4):-4]+'-mergerMinRanges.txt', dtype='int')
    '''MR=MergeRanges. MR[:,1]=merge ids, MR[:,2]=start frame, MR[:,3] = end'''
    X = np.array([])
    #Lets just use the first 10 mergers for now
    MR = MR[numUsing:2*numUsing]
    for row in MR:
        Xi = np.array([])
        for frame in range(row[1],row[2]):
            Xi = np.append(Xi,dictOfGrids[frame])
        #initPos = getStartVals(ID)
        #Xi = np.append(Xi, initPos)
        print(X)
        print(X.shape)
        print(Xi)
        Xi.shape = (1,len(Xi))
        if  X.shape == (0,):
            X = Xi
        else:
            X=np.append(X,Xi,axis=0)
    return X
    
def getY(filename):
    path = os.getcwd()+'/'
    IDDict = futil.LoadDictFromTxt(path+filename, 'vid')
    a = len('aug_trajectories-0750am-0805am.txt')
    MR = np.loadtxt(path+filename[:-a]+'mergeTrajectoryInfo/'+filename[(-a+4):-4]+'-mergerMinRanges.txt', dtype='int')
    MR = MR[:numUsing]
    Y = np.array([])    
    for row in MR:
        ID = row[0]
        yi = np.array([])
        dictOfFrames = IDDict[ID]
        for frame in range(row[1],row[2]):
            yi = np.append(yi,dictOfFrames[frame][LocalX:LocalY])
        print(Y)
        print(Y.shape)
        print(yi)
        yi.shape = (1,len(yi))
        if Y.shape == (0,):
            Y = yi
        else:
            Y = np.append(Y,yi,axis=0)
    return Y
    
def getX2(filename):
    

filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
Xtrain=getX(filename)
ytrain=getY(filename)
print(X.shape)
print(y.shape)
linmod1 = linear_model.LinearRegression()
linmod1.fit(X, y)
