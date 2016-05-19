import numpy as np
from lib import frame_util as futil
import sys, os


#Creates augmented trajectory files with Vy and Ay data
def augmentTrajectories():
	print("Calculating Vy, Ay...")
	vidDict = futil.AddVxAx("res/101_trajectories/trajectories-0750am-0805am.txt", "res/101_trajectories/aug_trajectories-0750am-0805am.txt")
	print("First trajectory file finished...")
	vidDict = futil.AddVxAx("res/101_trajectories/trajectories-0805am-0820am.txt", "res/101_trajectories/aug_trajectories-0805am-0820am.txt")
	print("Second trajectory file finished...")
	vidDict = futil.AddVxAx("res/101_trajectories/trajectories-0820am-0835am.txt", "res/101_trajectories/aug_trajectories-0820am-0835am.txt")
	print("Third trajectory file finished...")


def main(argv):
	augmentTrajectories()

if __name__ == "__main__":
    main(sys.argv)
