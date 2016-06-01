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

numUsing = 0 # 0 to use all

'''Returns the startX and startY for all merge vehicles'''
def getStartVals(filename):
    filepath = makePathMR(filename, '-mergerStartTrajectories')
    A = np.loadtxt(filepath)
    return A[:,[constants.LocalX,constants.LocalY]]

'''Removes the entry corresponding to this vid from the grid'''
def removeIDfromGrid(Frame, VID, Grid):
    vehicleTraj = Frame[VID]
    [xpos,ypos]=vehicleTraj[[constants.LocalX,constants.LocalY]]
    indexX, indexY = futil.GetGridIndices(xpos,ypos)
    if not Grid[indexX][indexY][0] == 0:
         Grid[indexX][indexY][0] = Grid[indexX][indexY][0]-1
         #recalculate velocities?
    else:
        # Gave error with =[0,0,0], apparently grid is of size 6 not 3...
        Grid[indexX][indexY] = [0,0,0,0,0,0]
    # Did not check all grids, but the first grid seems to be all 0's... seems wrong?
    return Grid

'''Called for each merging vehicle, gets all the input data.'''
def getXInner(row,dictOfGrids, initPos, dictOfFrames):
    VID = row[0]
    start = row[1]
    X_for_id = np.array([]) #This will have numFrames rows and sizeGrid+1 columns
    for frame in range(row[1],row[2]):
        t_elapsed = frame-start        
        grid = dictOfGrids[frame]
        grid = removeIDfromGrid(dictOfFrames[frame],VID,grid)
        Xrow = np.append(t_elapsed,grid.flatten())
        Xrow.shape = (1,len(Xrow))
        if X_for_id.shape == (0,):
            X_for_id = Xrow
        else:
            X_for_id = np.append(X_for_id,Xrow,axis=0)
    # Xi = np.append(Xi, initPos)
    # Xi.shape = (1,len(Xi))
    return (X_for_id)

'''Gets ground truths for each merge vehicle'''
def getYInner(row, dictOfFrames):
    y_for_id = np.array([]) #this will have numFrames rows and 1 column
    for frame in range(row[1],row[2]):
        yrow = dictOfFrames[frame][[constants.LocalX]]#,constants.LocalY]])
        y_for_id = np.append(y_for_id,yrow)
    return y_for_id

'''AVOID---This probably uses a significant amount of memory'''
def append(orig, add, axisNum=0):
    if orig.shape == (0,):
        orig = add
    else:
        orig = np.append(orig,add,axis=axisNum)
    return orig

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
    Xtrain = np.array([])   #will have numTrain*numFrames rows and size(grid)+1 columns
    Xtest = np.array([])
    it = 0
    trainEmpty = True
    testEmpty = True
    if not numUsing == 0:
        MR = MR[:numUsing]
    for row in MR:
        thisStart = start[it]
        XVID = sparse.csr_matrix(np.ascontiguousarray(getXInner(row, dictOfGrids,thisStart,frameDict)))
        if row[0] in trainIDs:
            if  trainEmpty == True:
                Xtrain = XVID
                trainEmpty = False
            else:
                Xtrain = sparse.vstack((Xtrain,XVID))#,axis=0)
            print("Finished getting X data for Merger with VID:",row[0]," and it is a training example")
        else:
            if testEmpty == True:
                Xtest = XVID
                testEmpty = False
            else:
                Xtest = sparse.vstack((Xtest,XVID))#np.append(Xtest,XVID,axis=0)
            print("Finished getting X data for Merger with VID:",row[0]," and it is a test example")
        it += 1
        print(Xtrain.shape)
    return Xtrain, Xtest
    
def getY(filename, trainIDs, testIDs):
    path = os.getcwd()+'/'
    IDDict = futil.LoadDictFromTxt(path+filename, 'vid')
    filepath = makePathMR(filename, '-mergerMinRanges')
    MR = np.loadtxt(filepath, dtype='int')
    Ytrain = np.array([])    #will have numTrain*numFrames rows and 1 column
    Ytest = np.array([])
    if not numUsing == 0:
        MR = MR[:numUsing]
    for row in MR:
        YVID = np.ascontiguousarray(getYInner(row,IDDict[row[0]]))
        if row[0] in trainIDs:
            Ytrain=append(Ytrain,YVID) #uses append because Y is small in memory
            print("Finished getting Y data for Merger with VID:",row[0]," and it is a training example")
        else:
            Ytest=append(Ytest,YVID)
            print("Finished getting Y data for Merger with VID:",row[0]," and it is a test example")
    return np.ascontiguousarray(Ytrain), np.ascontiguousarray(Ytest)
    
def makePathMR(filename, end):
    path = os.getcwd()+'/'
    a = len('aug_trajectories-0750am-0805am.txt')
    return path+filename[:-a]+filename[(-a+4):-4]+end+'.txt'

def getSpan(filename):
    return filename[-17:][:-4]
    
def makePathToTrajectories(filename):
    outerFolder = filename[4:-35]
    path1 = constants.PATH_TO_RESOURCES + '/' + outerFolder + '/' 
    return path1 + getSpan(filename) + '/'

def makeFullPath(filename, end):
    path = makePathToTrajectories
    return path + end

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

def saveSparse(filepath, X):
    data = X.data
    indices = X.indices
    indptr = X.indptr
    np.savetxt(filepath + '-data',data)
    np.savetxt(filepath + '-indices',indices)
    np.savetxt(filepath + '-indptr',indptr)

def loadSparse(filepath):
    data = np.loadtxt(filepath + '-data')
    indices = np.loadtxt(filepath + '-indices')
    indptr = np.loadtxt(filepath + '-indptr')
    return sparse.csr_matrix((data,indices,indptr))
    
def saveExampleData(filename,Xtrain,ytrain,Xtest,ytest):
    filepath_Xtrain = makeFullPath(filename, '-Xtrain')
    saveSparse(filepath_Xtrain[:-4], Xtrain)
    filepath_ytrain = makeFullPath(filename, '-ytrain')
    np.savetxt(filepath_ytrain, ytrain)
    filepath_Xtest = makeFullPath(filename, '-Xtest')
    saveSparse(filepath_Xtest[:-4], Xtest)
    filepath_ytest = makeFullPath(filename, '-ytest')
    np.savetxt(filepath_ytest, ytest)

def readExampleData(filename):
    filepath_Xtrain = makeFullPath(filename, '-Xtrain')
    Xtrain = loadSparse(filepath_Xtrain[:-4])
    print("Xtrain loaded.")
    filepath_Xtest = makeFullPath(filename, '-Xtest')
    Xtest = loadSparse(filepath_Xtest[:-4])
    print("Xtest loaded.")
    filepath_ytrain = makeFullPath(filename, '-ytrain')
    ytrain = np.loadtxt(filepath_ytrain)
    print("ytrain loaded.")
    filepath_ytest = makeFullPath(filename, '-ytest')
    ytest = np.loadtxt(filepath_ytest)
    print("ytest loaded.")
    return Xtrain, ytrain, Xtest, ytest
    