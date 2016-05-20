# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:26:40 2016

@author: Derek
"""
import numpy as np

def makeTrainTestData(filepath, portion):
    #filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"
    MR = np.loadtxt(filepath, dtype='int')
    train = []
    test = []
    for ID in MR:
        if random() > portion:
            test = test.append(ID)
        else:
            train = train.append(ID)
    return train, test

    