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
import random

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

numUsing = 100

def getStartVals(filename):
    filepath = makePathMR(filename, '-mergerStartTrajectories')
    A = np.loadtxt(filepath)
    return A[:,[LocalX,LocalY]]

def getX2(row, X,dictOfGrids, initPos):
    Xi = np.array([])
    for frame in range(row[1],row[2]):
        Xi = np.append(Xi,dictOfGrids[frame])
    Xi = np.append(Xi, initPos)
    Xi.shape = (1,len(Xi))
    if  X.shape == (0,):
        X = Xi
    else:
        X=np.append(X,Xi,axis=0)
    return X

def getY2(row, Y, dictOfFrames):
    yi = np.array([])
    for frame in range(row[1],row[2]):
        yi = np.append(yi,dictOfFrames[frame][LocalX:LocalY])
    yi.shape = (1,len(yi))
    if Y.shape == (0,):
        Y = yi
    else:
        Y = np.append(Y,yi,axis=0)
    return Y

#get the training examples
def getX(filename, trainIDs, testIDs):
    #filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
    path = os.getcwd()+'/'
    frameDict = futil.LoadDictFromTxt(path+filename, 'frame')
    dictOfGrids = futil.GetGridsFromFrameDict(frameDict)
    filepath = makePathMR(filename, '-mergerMinRanges')
    MR = np.loadtxt(filepath, dtype='int')
    '''MR=MergeRanges. MR[:,0]=merge ids, MR[:,1]=start frame, MR[:,2] = end'''
    start = getStartVals(filename)    
    Xtrain = np.array([])  
    Xtest = np.array([])
    it= 0
    if not numUsing == 0:
        MR = MR[:numUsing]
    for row in MR:
        thisStart = start[it]
        if row[0] in trainIDs:
            Xtrain = getX2(row, Xtrain, dictOfGrids,thisStart)
        else:
            Xtest = getX2(row, Xtest, dictOfGrids, thisStart)
        it += 1
    return sparse.csr_matrix(Xtrain), sparse.csr_matrix(Xtest)
    
def getY(filename, trainIDs, testIDs):
    path = os.getcwd()+'/'
    IDDict = futil.LoadDictFromTxt(path+filename, 'vid')
    filepath = makePathMR(filename, '-mergerMinRanges')
    MR = np.loadtxt(filepath, dtype='int')
    Ytrain = np.array([])    
    Ytest = np.array([])
    if not numUsing == 0:
        MR = MR[:numUsing]
    for row in MR:
        if row[0] in trainIDs:
            Ytrain = getY2(row,Ytrain,IDDict[row[0]])
        else:
            Ytest = getY2(row, Ytest,IDDict[row[0]])
    return Ytrain, Ytest
    
def makePathMR(filename, end):
    path = os.getcwd()+'/'
    a = len('aug_trajectories-0750am-0805am.txt')
    return path+filename[:-a]+'mergeTrajectoryInfo/'+filename[(-a+4):-4]+end+'.txt'

def makeTrainTestData(filepath, portionTrain):
    #filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
    filepath = makePathMR(filename, '-mergerMinRanges')
    MR = np.loadtxt(filepath, dtype='int')
    traintest = [[],[]]
    for ID in MR[:,0]:
        traintest[random.random() > portionTrain].append(ID)
    train = traintest[0]
    test = traintest[1]
    return train, test
    

filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
trainIDs, testIDs = makeTrainTestData(makePathMR(filename, '-mergerMinRanges'), .75)
Xtrain, Xtest =getX(filename, trainIDs, testIDs)
print(Xtrain.shape)
print(Xtest.shape)
ytrain, ytest =getY(filename, trainIDs, testIDs)
print(ytrain.shape)
print(ytest.shape)
linmod1 = linear_model.LinearRegression()
linmod1.fit(Xtrain, ytrain)
predictions = linmod1.predict(Xtest)
score = (linmod1.score(Xtest,ytest))
check = (linmod1.score(Xtrain,ytrain))
np.savetxt(makePathMR(filename, 'ACTUALS'+str(numUsing)+'.txt'), ytest)
np.savetxt(makePathMR(filename,'PREDICTIONS' +str(numUsing) + '.txt'), predictions)
np.savetxt(makePathMR(filename,'SCORE' +str(numUsing) + '.txt'), [score, check])


