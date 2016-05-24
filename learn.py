# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:14:54 2016

@author: Derek
"""

import numpy as np
from lib import learn_util

#This will probably have to be made better at some point
filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"


#if xtrain has not been loaded, do that
trainIDs, testIDs = learn_util.makeTrainTestData(filename, .75)
Xtrain, Xtest = learn_util.getX(filename, trainIDs, testIDs)
print(Xtrain.shape)
print(Xtest.shape)
ytrain, ytest = learn_util.getY(filename, trainIDs, testIDs)
print(ytrain.shape)
print(ytest.shape)


#actual learn stuff
predictions = []
ytests = []
from sklearn import svm
svmR = svm.SVR(kernel='rbf')
for i in range(len(ytrain[0])):
    #train model on Xtrain, ytrain[:,i]
    svmR.fit(Xtrain,ytrain[:,i])
    ypredict = svmR.predict(Xtest)
    if i % 10 == 0:
        print(ypredict)
        print(ytest[:,i])
    ytests.append(ytest[:,i])
    predictions.append(ypredict)
diff = np.array(ytests)-np.array(predictions)
norm = np.linalg.norm(diff)
print(diff)
print(norm)
    
'''linmod1 = linear_model.LinearRegression()
linmod1.fit(Xtrain, ytrain)
predictions = linmod1.predict(Xtest)
score = (linmod1.score(Xtest,ytest))
check = (linmod1.score(Xtrain,ytrain))
if numUsing == 0:
    numUsing == 'ALL'
np.savetxt(makePathMR(filename, 'ACTUALS'+str(numUsing)+'.txt'), ytest)
np.savetxt(makePathMR(filename,'PREDICTIONS' +str(numUsing) + '.txt'), predictions)
np.savetxt(makePathMR(filename,'SCORE' +str(numUsing) + '.txt'), [score, check])

from sklearn.externals import joblib
joblib.dump(linmod1, makePathMR(filename,'MODEL' +str(numUsing) + '.pkl'))'''