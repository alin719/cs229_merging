import numpy as np
from lib import frame_util as futil
from lib import merger_methods as mm
from lib import constants

import sys, os

#Creates augmented trajectory files with Vy and Ay data
def augmentTrajectories():
	print("Calculating Vy, Ay for 101 dataset...")
	vidDict = futil.AddVxAx("res/101_trajectories/trajectories-0750am-0805am.txt", "res/101_trajectories/aug_trajectories-0750am-0805am.txt")
	print("First trajectory file finished...")
	vidDict = futil.AddVxAx("res/101_trajectories/trajectories-0805am-0820am.txt", "res/101_trajectories/aug_trajectories-0805am-0820am.txt")
	print("Second trajectory file finished...")
	vidDict = futil.AddVxAx("res/101_trajectories/trajectories-0820am-0835am.txt", "res/101_trajectories/aug_trajectories-0820am-0835am.txt")
	print("Third trajectory file finished...")

def findMergers():
    print("Finding merger vehicle information...")
    for (filepath, filename) in constants.paths:
        open(filepath+'.txt', 'r')
        print("Starting merge stuff for:", filepath+'.txt')
        #mm.doMinRangesAndStartForMerges(filepath, constants.LaneID, constants.VehicleID,
        #                                constants.FrameID, constants.TotFrames) #MergeLane=7
        if 'compressed' in filename:
                mm.doRangesAndStartForMerges(filepath, 9, constants.VehicleID,
                                        constants.FrameID, constants.TotFrames,
                                        filename) #MergeLane=7
        else:
            mm.doRangesAndStartForMerges(filepath, constants.LaneID, constants.VehicleID,
                                        constants.FrameID, constants.TotFrames,
                                        filename) #MergeLane=7

def main(argv):
    #augmentTrajectories()
    findMergers()

if __name__ == "__main__":
    main(sys.argv)
