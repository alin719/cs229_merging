import numpy as np
import matplotlib.pyplot as plt
import time
import pylab as pl
import importlib
from lib import util
import learn_util
from copy import deepcopy
import os
from lib import frame_util as futil

##Example usage at bottom.


def visualizePredictions(predFilename, actualFilename):
    predFile = open(predFilename)
    predLines = predFile.readlines()
    predArray = np.array(predLines).astype(float)
    predFile.close()
    actualFile = open(actualFilename)
    actualLines = actualFile.readlines()
    actualArray = np.array(actualLines).astype(float)
    actualFile.close()
    diff = predArray - actualArray
    x_axis = np.array(range(len(predArray)))
    return x_axis, predArray, actualArray, diff
    
      
def outputFigures(outerFolderName, subfolderName):
    #Input parameter example: subfolderName = "SVM-default=1-default=0.1_06-02-2016_12h-59m-52s-selected/"
    targetFolderName = outerFolderName + subfolderName + "/"
    actualFilename = targetFolderName + "ACTUALS-TEST.txt"
    predFilename = targetFolderName + "PREDICTIONS-TEST.txt"
    figuresFolder = "Figures/"
    if not os.path.exists(targetFolderName + figuresFolder):
        os.makedirs(targetFolderName + figuresFolder)

    x, pred, actual, diff = visualizePredictions(predFilename, actualFilename)
    
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 16
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size
    EXAMPLE_SIZE = 254

    for trial in range(25):
        curDiff = abs(diff[trial*EXAMPLE_SIZE: (trial+1)*EXAMPLE_SIZE])
        loss = np.sum(curDiff)
        avgLoss = np.mean(curDiff)
        plt.plot(x, pred, label='pred')
        plt.plot(x, actual, label='actual')
        plt.xlabel("Frame (timestep)")
        plt.ylabel("Y Position")

        #titleString = "Merge Vehicle #" + str(trial) +  ", Loss = " + str(loss) + " ft, Avg Loss = " + str(avgLoss) + " ft"
        titleString = "Merge Vehicle #" + str(trial) +  ", Average Loss = " + str(avgLoss) + " ft"
        plt.title(titleString)
        plt.legend()
        plt.axis([trial*EXAMPLE_SIZE, (trial+1)*EXAMPLE_SIZE, 20, 120])
        targetFile = "trial" + str(trial)
        extension = ".png"
        targetFileName = targetFolderName + figuresFolder + targetFile + extension
        plt.savefig(targetFileName)
        plt.clf()
    totalAverageLoss = np.mean(abs(diff))
    totalLossFile = open(targetFolderName + figuresFolder + str(totalAverageLoss) + "_avgloss.txt", 'w')
    totalLossFile.write("Average Loss = " + str(totalAverageLoss))
    print("Output figures and loss to " + targetFolderName + figuresFolder)

#Example usage
outerFolderName = "results/Trial1/"
for subfolder in os.listdir(outerFolderName):
    outputFigures(outerFolderName, subfolder)