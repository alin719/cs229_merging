import collections, itertools, copy
import numpy, scipy, math, random
import os, sys, time, importlib
import tokenize, re, string
import json, unicodedata

PATH_TO_ROOT = None
PATH_TO_RESOURCES = None
PATH_TO_EXECUTABLES = None
PATH_TO_LIBRARIES = None
EXECUTABLES = None
EXE_ARG_POS = None
DEFAULT_EXE_CHOICE = None
GRID_X = 2250
GRID_Y = 70
X_DIVS = 225
Y_DIVS = 35


##
# Function: init
# -------------------
# Because of some weird bug with __file and absolute vs. relative paths,
# constants.py must have a separate function to actually configure the
# global constants, using a path_to_root variable fed to it by __main__.py.
#
# Example path_to_root on my computer:
#   "/Users/austin_ray/GitHub/cs221-project/recipe_writer"
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


	# This is the absolute path of the recipe_writer folder on your computer.
	PATH_TO_ROOT = pathToRoot

	# The full paths of the folders holding various important things
	PATH_TO_RESOURCES = os.path.join(PATH_TO_ROOT, "res")
	PATH_TO_EXECUTABLES = os.path.join(PATH_TO_ROOT, "bin")
	PATH_TO_LIBRARIES = os.path.join(PATH_TO_ROOT, "lib")

	# Used by:
	#  - main.py to direct execution to the proper executable in bin/
	EXECUTABLES = ["setup", "sandbox"]
	EXE_ARG_POS = 1

