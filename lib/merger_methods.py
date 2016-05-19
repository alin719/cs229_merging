# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:48:22 2016

@author: Derek
"""
import numpy as np

def unique(a):
    b = np.diff(a)
    b=np.r_[1,b]
    return a[b != 0]

def findFirstInstances(Data, VIDCol):
    d = {}
    for row in Data:
        key = row[VIDCol]
        if key not in d:
            d[key] = row
    return np.array(list(d.values()))
    
def getMergersFullData(Data, Firsts, LaneCol, MergeLane, VIDCol):
     Mergers = Firsts[Firsts[:,LaneCol]==MergeLane]
     d2 = []
     for row in Data:
        key = row[VIDCol]
        if key in Mergers[:,VIDCol]:
            d2.append(row)
     return np.array(d2)

def findMergerFullTraj(filepath, LaneCol, MergeLane, VIDCol):
    Data = np.loadtxt(filepath+'.txt')
    Firsts = findFirstInstances(Data, VIDCol)      
    return getMergersFullData(Data, Firsts, LaneCol, MergeLane, VIDCol)
    
def getMergerIDs(mergerFullData,VIDCol):
    return unique(mergerFullData[:,VIDCol])
    
def saveArrayTxt(filepath, array, fmt='%d'):
    np.savetxt(filepath, array, fmt=fmt)
    
def findAndSaveMergerTrajectories(filepath, LaneCol, MergeLane, VIDCol):    
    mergerFullData = findMergerFullTraj(filepath, LaneCol, MergeLane, VIDCol)
    saveArrayTxt(filepath+'-mergers'+'.txt', mergerFullData, fmt='%f')
    
def findAndSaveMergeIDs(filepath, LaneCol, MergeLane, VIDCol):  
    mergerFullData = findMergerFullTraj(filepath, LaneCol, MergeLane, VIDCol)
    saveArrayTxt(filepath+'-mergerIDs'+'.txt', getMergerIDs(mergerFullData,VIDCol))

def findMergeEventRanges(filepath, LaneCol, MergeLane, VIDCol, FrameCol, TotFrameCol):
    #This will find, for each VID that merges, the start and end frames
    Data = np.loadtxt(filepath+'.txt')
    Firsts = findFirstInstances(Data, VIDCol)  
    Starts = Firsts[:,FrameCol]
    Ends = Starts + Firsts[:,TotFrameCol]
    Ends.shape=(len(Ends),1)
    IDStarts = Firsts[:,[VIDCol,FrameCol]]
    Ranges = np.append(IDStarts, Ends, axis=1)
    return Ranges

def findAndSaveMergeEventRanges(filepath, LaneCol, MergeLane, VIDCol, FrameCol, TotFrameCol):
    Ranges =  findMergeEventRanges(filepath, LaneCol, MergeLane, VIDCol, FrameCol, TotFrameCol)
    saveArrayTxt(filepath+'-mergerRanges'+'.txt', Ranges)
    
    #mergerFullData = Data[Data[:,VehicleID] in list(Mergers[:,VehicleID])]
    #mergerTrajData = mergerFullData[:,[VehicleID, FrameID, LocalX, LocalY, Vel, Accel, LaneID]]
    #print(mergerFullData)
    
def findMergeEventRangesMin(filepath, LaneCol, MergeLane, VIDCol, FrameCol, TotFrameCol):
    #This will find, for each VID that merges, the start and end frames based on the minimum number of frames any merge appears in
    Data = np.loadtxt(filepath+'.txt')
    Firsts = findFirstInstances(Data, VIDCol)  
    Starts = Firsts[:,FrameCol]
    Ends = Starts + min(Firsts[:,TotFrameCol])
    Ends.shape=(len(Ends),1)
    IDStarts = Firsts[:,[VIDCol,FrameCol]]
    Ranges = np.append(IDStarts, Ends, axis=1)
    return Ranges

def findAndSaveMergeEventRanges(filepath, LaneCol, MergeLane, VIDCol, FrameCol, TotFrameCol):
    Ranges =  findMergeEventRangesMin(filepath, LaneCol, MergeLane, VIDCol, FrameCol, TotFrameCol)
    saveArrayTxt(filepath+'-mergerMinRanges'+'.txt', Ranges)