import collections, itertools, copy
import numpy, scipy, math, random
import os, sys, time, importlib
import tokenize, re, string
import json, unicodedata
from lib import learn_util as lu

VehicleID = 1-1
FrameID = 2-1
TotFrames = 3-1
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



path101 = os.getcwd()+'/res/101_trajectories/'
path80 = os.getcwd()+'/res/80_trajectories/'

file101_1 = 'aug_trajectories-0750am-0805am'
file101_2 = 'aug_trajectories-0805am-0820am'
file101_3 = 'aug_trajectories-0820am-0835am'
file101 = '101_full_trajectories_compressed'
file80_1 = 'aug_trajectories-0400-0415'
file80_2 = 'aug_trajectories-0500-0515'
file80_3 = 'aug_trajectories-0515-0530'
paths=[#(path101+file101_1[4:],'res/101_trajectories/'+file101_1+'.txt'), 
       #(path101+file101_2[4:],'res/101_trajectories/'+file101_2+'.txt'),
       #(path101+file101_3[4:],'res/101_trajectories/'+file101_3+'.txt'),
       (path101+file101,'res/101_trajectories/'+file101+'.txt')]
       #,path80+file80_1, path80+file80_2, path80+file80_3]


PATH_TO_ROOT = None
PATH_TO_RESOURCES = os.getcwd() + '/res'
PATH_TO_EXECUTABLES = None
PATH_TO_LIBRARIES = None
EXECUTABLES = None
EXE_ARG_POS = None
DEFAULT_EXE_CHOICE = None
MAX_X = 70
MAX_Y = 2250

X_DIV = 10
Y_DIV = 60
MIN_GRID_X = 0
MAX_GRID_X = 40
MIN_GRID_Y = 0
MAX_GRID_Y = 1500
X_STEP = float((MAX_GRID_X - MIN_GRID_X)/X_DIV)
Y_STEP = float((MAX_GRID_Y - MIN_GRID_Y)/Y_DIV)

# X_DIV = 35
# Y_DIV = 200
# X_STEP = float(MAX_X/X_DIV)
# Y_STEP = float(MAX_Y/Y_DIV)

##
# Function: init
# -------------------
# Because of some weird bug with __file and absolute vs. relative paths,
# constants.py must have a separate function to actually configure the
# global constants, using a path_to_root variable fed to it by __main__.py.
#
# Example path_to_root on my computer:
#   "/Users/Alex Lin/Documents/CS229/Project/cs229_merging"
##
def init(pathToRoot):
    global PATH_TO_ROOT
    global PATH_TO_RESOURCES
    global PATH_TO_EXECUTABLES
    global PATH_TO_LIBRARIES
    global EXECUTABLES
    global EXE_ARG_POS
    global DEFAULT_EXE_CHOICE
    global GRID_X
    global GRID_Y
    global X_DIVS
    global Y_DIVS
    global X_STEP
    global Y_STEP

    # This is the absolute path of the recipe_writer folder on your computer.
    PATH_TO_ROOT = pathToRoot

    # The full paths of the folders holding various important things
    PATH_TO_RESOURCES = os.path.join(PATH_TO_ROOT, "res")
    PATH_TO_EXECUTABLES = os.path.join(PATH_TO_ROOT, "bin")
    PATH_TO_LIBRARIES = os.path.join(PATH_TO_ROOT, "lib")

    # Used by:
    #  - main.py to direct execution to the proper executable in bin/
    EXECUTABLES = ["setup", "sandbox", "visualize"]
    EXE_ARG_POS = 1

