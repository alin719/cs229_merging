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
import os



#This will probably have to be made better at some point
filename="res/101_trajectories/aug_trajectories-0750am-0805am.txt"

repickTrainTest = 1 #change if just want to recalculate and train/testIDs are in memory
remakeData = 1 #change to 0 after loaded first time, 0 to read, -1 to use memory

#if xtrain has not been loaded, do that

if remakeData == 1:
    if repickTrainTest == 1:
        trainIDs, testIDs = learn_util.makeTrainTestData(filename, .75)
    print("Recalculating all data",time.ctime())
    Xtrain, Xtest = learn_util.getX(filename, trainIDs, testIDs)
    print("Finished gathering and formatting X data",time.ctime())
    ytrain, ytest = learn_util.getY(filename, trainIDs, testIDs)
    print("Finished gathering and formatting Y data",time.ctime())
    learn_util.saveExampleData(filename, Xtrain, ytrain, Xtest, ytest)
elif remakeData == 0:
    print("Loading data from file...",time.ctime())
    Xtrain, ytrain, Xtest, ytest = learn_util.readExampleData(filename)

print(Xtrain.shape)
print(Xtest.shape)
print(ytrain.shape)
print(ytest.shape)
#otherwise, read from files


    
#run this after the model is fit
#if using a model with specific values (like penalties), include that in type
def saveModelStuff(model, modelType, Xtest, ytest, Xtrain, ytrain, filename): #modelType = 'SVM'     
    print("Done fitting model, getting predictions...", time.ctime())
    predictions = model.predict(Xtest)
    print ("Done with predictions, scoring...", time.ctime())    
    score = svmR.score(Xtest,ytest)
    print("Done with all prediction, saving outputs.", time.ctime())
    subfolder = util.string_appendDateAndTime(modelType) + '/'
    path = learn_util.makePathToTrajectories(filename) + subfolder
  
    np.savetxt(path + 'ACTUALS-TEST.txt', ytest)
    np.savetxt(path + 'PREDICTIONS-TEST.txt', predictions)
    np.savetxt(path + 'SCORE-TEST.txt', score)    
    #print ("Getting predictions on train data...", time.ctime())    
    #predictionsTrain = model.predict(Xtrain)
    print ("Done with predictions, scoring...", time.ctime())    
    check = svmR.score(Xtrain,ytrain)
      
    #np.savetxt(path + 'ACTUALS-TRAIN.txt', ytrain)
    #np.savetxt(path + 'PREDICTIONS-TRAIN.txt', predictionsTrain)
    np.savetxt(path + 'SCORE-TRAIN.txt', check)
    
    joblib.dump(model, path + 'MODEL')
    print('model ', modelType, ': score = ', score, 'train_score = ', check)
    

#actual learn stuff
# def saveModelStuff(model, modelType='SVM', Xtest, ytest, filename):
#     predictions = model.predict(Xtest)
#     score = svmR.score(Xtest,ytest)


#actual learn stuff
#diff = ytest-np.array(predictions)
#norm = np.linalg.norm(diff)
#outputsSVM = [['def','def',score,check,norm]] #already been computed
svmR = svm.SVR(cache_size=1500) #default,
print("Fitting default model...", time.ctime())
svmR.fit(Xtrain,ytrain)
saveModelStuff(svmR, 'SVM-default-default', Xtest, ytest, Xtrain, ytrain, filename)
for penalties in [10,100,10000]:
    for eps in [0.0001,0.000001]:
        svmR = svm.SVR(C=penalties,epsilon=eps,cache_size=1500) #kernel='rbf',
        print("Fitting svm model...", time.ctime())
        svmR.fit(Xtrain,ytrain)
        saveModelStuff(svmR, 'SVM-'+str(penalties)+'-'+str(eps), Xtest, ytest, Xtrain, ytrain, filename)

linmod1 = linear_model.LinearRegression() #aka least squares
print("Fitting linreg model...", time.ctime())
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