# cs229_merging

1) Setup

- Create the folders /res/101_trajectories and /res/80_trajectories
- Copy the raw trajectories in there.
- Go to the main directory, run python __main__.py setup
- This should take some time, but will calculate the Vx, Vys
  and output them.

2) Accessing Frame and Grid Data
- Use LoadDictFromText(filename, type) to load frame dictionary if
not already in memory.  type = 'vid' or 'frame'
- Once you have the frame dictionary, can call
 GetGridsFromFrameDict(frameDict) to get a dictionary of grids where
 the keys are Frame IDs and the values are an (X_DIV, Y_DIV, features)
 np array.  Features will be [x, y, Vx, Vy, Ax, Ay] of the vehicle
 at that point in the grid.
- Grid size can be changed by modifying values in constants.py

3) vehicleclass.py
- Makes it easier/more clear than accessing array indices.  Currently
the dictionaries are not stored as vehicles, but you can init a vehicle
from any entry, and then pull info from that.  Future updates include
using these directly in the dicts.

4) use learn.py as to learn. Can comment out the loading of
the data (indicated in script) once the various arrays are in memory. 
-The script will either compute and save the Xtrain/ytrain/Xtest/ytest data
to a file or read from it, make sure to indicate which you want by 
commenting out the other option
-Rerun it if you clear the memory or kernel at any point.

TODO:
- Write functions to save / load grids as txt files.
- Clean this shit up.

 Recap:
 Current pipeline for loading grids is:
 LoadDataFromTxt -> GetGridsFromFrameDict, then access using frame IDs.
