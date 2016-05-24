# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:11:36 2016

@author: Derek
"""

from lib import frame_util as futil
import numpy as np
import os
from scipy import sparse
from random import random
from lib import constants

numUsing = 0 #0 to use all


def getStartVals(filename):
    filepath = makePathMR(filename, '-mergerStartTrajectories')
    A = np.loadtxt(filepath)
    return A[:,[constants.LocalX,constants.LocalY]]

def getXInner(row, X,dictOfGrids, initPos):
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

def getYInner(row, Y, dictOfFrames):
    yi = np.array([])
    for frame in range(row[1],row[2]):
        yi = np.append(yi,dictOfFrames[frame][[constants.LocalX,constants.LocalY]])
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
    it = 0
    if not numUsing == 0:
        MR = MR[:numUsing]
    for row in MR:
        thisStart = start[it]
        if row[0] in trainIDs:
            Xtrain = getXInner(row, Xtrain, dictOfGrids,thisStart)
        else:
            Xtest = getXInner(row, Xtest, dictOfGrids, thisStart)
        it += 1
    return sparse.csr_matrix(np.ascontiguousarray(Xtrain)), sparse.csr_matrix(np.ascontiguousarray(Xtest))
    
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
            Ytrain = getYInner(row,Ytrain,IDDict[row[0]])
        else:
            Ytest = getYInner(row, Ytest,IDDict[row[0]])
    return np.ascontiguousarray(Ytrain), np.ascontiguousarray(Ytest)
    
def makePathMR(filename, end):
    path = os.getcwd()+'/'
    a = len('aug_trajectories-0750am-0805am.txt')
    return path+filename[:-a]+filename[(-a+4):-4]+end+'.txt'

def makeTrainTestData(filename, portionTrain):
    # example filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
    filepath = makePathMR(filename, '-mergerMinRanges')
    MR = np.loadtxt(filepath, dtype='int')
    traintest = [[],[]]
    if not numUsing == 0:
        MR = MR[:numUsing]
    for row in MR:
        traintest[random() > portionTrain].append(row[0])
    train = traintest[0]
    test = traintest[1]
    return train, test

def saveExampleData(filename,Xtrain,ytrain,Xtest,ytest):
    filepath_Xtrain = makePathMR(filename, 'Xtrain')
    np.savetxt(filepath_Xtrain, Xtrain)
    filepath_ytrain = makePathMR(filename, 'ytrain')
    np.savetxt(filepath_ytrain, ytrain)
    filepath_Xtest = makePathMR(filename, 'Xtest')
    np.savetxt(filepath_Xtest, Xtest)
    filepath_ytest = makePathMR(filename, 'ytest')
    np.savetxt(filepath_ytest, ytest)

def readExampleData(filename):
    filepath_Xtrain = makePathMR(filename, 'Xtrain')
    Xtrain = np.loadtxt(filepath_Xtrain)
    filepath_Xtest = makePathMR(filename, 'Xtest')
    Xtest = np.loadtxt(filepath_Xtest)
    filepath_ytrain = makePathMR(filename, 'ytrain')
    ytrain = np.loadtxt(filepath_ytrain)
    filepath_ytest = makePathMR(filename, 'ytest')
    ytest = np.loadtxt(filepath_ytest)
    return Xtrain, ytrain, Xtest, ytest
    