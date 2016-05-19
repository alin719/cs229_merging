# cs229_merging

1) Setup

- Create the folder /res/101_trajectories
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


 Recap:
 Current pipeline for loading grids is:
 LoadDataFromTxt -> GetGridsFromFrameDict, then access using frame IDs.