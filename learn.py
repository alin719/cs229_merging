# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:14:54 2016

@author: Derek
"""

import numpy as np
from lib import learn_util
import sys

#This will probably have to be made better at some point
filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"

remakeData=0 #change to 0 after loaded first time

#if xtrain has not been loaded, do that

if remakeData == 1:
    trainIDs, testIDs = learn_util.makeTrainTestData(filename, .75)
    Xtrain, Xtest = learn_util.getX(filename, trainIDs, testIDs)
    print("Finished gathering and formatting X data")
    ytrain, ytest = learn_util.getY(filename, trainIDs, testIDs)
    print("Finished gathering and formatting Y data")
    learn_util.saveExampleData(filename, Xtrain, ytrain, Xtest, ytest)
else:
    print("Loading data from file...")
    Xtrain, ytrain, Xtest, ytest = learn_util.readExampleData(filename)

print(Xtrain.shape)
print(Xtest.shape)
print(ytrain.shape)
print(ytest.shape)
#otherwise, read from files


'''#actual learn stuff
predictions = []
ytests = []
scores = []
from sklearn import svm
svmR = svm.SVR(C=sys.float_info.max,epsilon=sys.float_info.min, cache_size=500, gamma=0.001) #kernel='rbf',
#followed advicef rom http://stackoverflow.com/questions/34475245/sklearn-svm-svr-and-svc-getting-the-same-prediction-for-every-input
#Doesnt seem to be working though. Myabe you can take a crack at it?
for i in range(len(ytrain[0])):
    #train model on Xtrain, ytrain[:,i]
    svmR.fit(Xtrain,ytrain[:,i])
    ypredict = svmR.predict(Xtest)
    if i % 15 == 0:
        print('Currently on iteration:', i)
        print('Predictions:',ypredict)
        print('Actuals:',ytest[:,i])
    ytests.append(ytest[:,i])
    predictions.append(ypredict)
    scores.append(svmR.score(Xtest,ytest[:,i]))
diff = np.array(ytests)-np.array(predictions)
norm = np.linalg.norm(diff)
print(diff)
print(norm)
print (scores)
print (max(scores))
print (min(scores))
    
linmod1 = linear_model.LinearRegression()
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