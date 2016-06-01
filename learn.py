# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:14:54 2016

@author: Derek
"""

import numpy as np
from lib import learn_util
from lib import util
from lib import constants as c
import sys
import time
from sklearn.externals import joblib
from sklearn import svm
from sklearn import linear_model



#This will probably have to be made better at some point
filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"

repickTrainTest = 1 #change if just want to recalculate and train/testIDs are in memory
remakeData = 1 #change to 0 after loaded first time, 0 to read, -1 to use memory

#if xtrain has not been loaded, do that

if remakeData == 1:
    if repickTrainTest == 1:
        trainIDs, testIDs = learn_util.makeTrainTestData(filename, .75)
    print("Recalculating all data")
    Xtrain, Xtest = learn_util.getX(filename, trainIDs, testIDs)
    print("Finished gathering and formatting X data")
    ytrain, ytest = learn_util.getY(filename, trainIDs, testIDs)
    print("Finished gathering and formatting Y data")
    learn_util.saveExampleData(filename, Xtrain, ytrain, Xtest, ytest)
elif remakeData == 0:
    print("Loading data from file...")
    Xtrain, ytrain, Xtest, ytest = learn_util.readExampleData(filename)

print(Xtrain.shape)
print(Xtest.shape)
print(ytrain.shape)
print(ytest.shape)
#otherwise, read from files

#run this after the model is fit
#if using a model with specific values (like penalties), include that in type
def saveModelStuff(model, modelType, Xtest, ytest, Xtrain, ytrain, filename): #modelType = 'SVM'     
    print("Done fitting model, getting prdeictions...", time.ctime())
    predictions = model.predict(Xtest)
    print ("Done with predictions, scoring...", time.ctime())    
    score = svmR.score(Xtest,ytest)
    print ("Getting prdeictions on train data...", time.ctime())    
    predictionsTrain = model.predict(Xtrain)
    print ("Done with predictions, scoring...", time.ctime())    
    check = svmR.score(Xtrain,ytrain)
    print("Done with all prediction, saving outputs.", time.ctime())
    folder = util.string_appendDateAndTime(learn_util.getSpan(filename)) + modelType + '/'
    path = c.PATH_TO_RESOURCES + '/101_trajectories/' + folder
    print('model ', modelType, ': score = ', score, 'train_score = ', check)
    np.savetxt(path + 'ACTUALS', ytest)
    np.savetxt(path + 'PREDICTIONS-TEST', predictions)
    np.savetxt(path + 'PREDICTIONS-TRAIN', predictionsTrain)
    np.savetxt(path + 'SCORE-TEST', score)
    np.savetxt(path + 'SCORE-TRAIN', check)
    joblib.dump(model, path + 'MODEL')

#actual learn stuff
# def saveModelStuff(model, modelType='SVM', Xtest, ytest, filename):
#     predictions = model.predict(Xtest)
#     score = svmR.score(Xtest,ytest)


#actual learn stuff
#diff = ytest-np.array(predictions)
#norm = np.linalg.norm(diff)
#outputsSVM = [['def','def',score,check,norm]] #already been computed
for penalties in [10, 100,1000,10000]:
    for eps in [0.0001,0.00001,0.000001]:
        svmR = svm.SVR(C=penalties,epsilon=eps,cache_size=1500) #kernel='rbf',
        print("Fitting Model...", time.ctime())
        svmR.fit(Xtrain,ytrain)
        saveModelStuff(svmR, 'SVM-'+penalties+'-'+eps, Xtest, ytest, Xtrain, ytrain, filename)

linmod1 = linear_model.LinearRegression()
linmod1.fit(Xtrain, ytrain)
saveModelStuff(linmod1, 'linReg', Xtest, ytest, Xtrain, ytrain, filename)
#from sklearn import linear_model
#linmod1 = linear_model.LinearRegression()
#linmod1.fit(Xtrain, ytrain)




'''#followed advicef rom http://stackoverflow.com/questions/34475245/sklearn-svm-svr-and-svc-getting-the-same-prediction-for-every-input
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
    
from sklearn import linear_model
linmod1 = linear_model.LinearRegression()
linmod1.fit(Xtrain, ytrain)
predictions = linmod1.predict(Xtest)
score = (linmod1.score(Xtest,ytest))
check = (linmod1.score(Xtrain,ytrain))
if numUsing == 0:
    numUsing == 'ALL'
np.savetxt(makePathMR(filename, '-ACTUALS-'+str(numUsing)), ytest)
np.savetxt(makePathMR(filename,'-PREDICTIONS-' +str(numUsing)), predictions)
np.savetxt(makePathMR(filename,'-SCORE-' +str(numUsing)), [score, check])

from sklearn.externals import joblib
joblib.dump(linmod1, makePathMR(filename,'-MODEL-' +str(numUsing)))'''