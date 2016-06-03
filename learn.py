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

repickTrainTest = 0 #1 to recalulate, 0 to load, -1 to use memory
seed = None
remakeData = 1 #1 to recalulate, 0 to load, -1 to use memory
mean_centered = 1 #1 to mean center, 0 to not mean center
predict = 'X' #'Y' or 'X'

if repickTrainTest == 1:
    trainIDs, testIDs = learn_util.makeTrainTestData(filename, .75, seed)
elif repickTrainTest == 0:
    trainIDs, testIDs = learn_util.loadTrainTestData(filename)

if remakeData == 1:
    print("Recalculating all data, mean_centered =",mean_centered,"predicting",predict,"position.")
    print("started at",time.ctime())
    Xtrain, Xtest = learn_util.getX(filename, trainIDs, testIDs, mean_centered)
    print("Finished gathering and formatting X data",time.ctime())
    ytrain, ytest = learn_util.getY(filename, trainIDs, testIDs, predict)
    print("Finished gathering and formatting Y data",time.ctime())
    learn_util.saveExampleData(filename, Xtrain, ytrain, Xtest, ytest, mean_centered, predict)
elif remakeData == 0:
    print("Loading data from file...",time.ctime())
    Xtrain, ytrain, Xtest, ytest = learn_util.readExampleData(filename, mean_centered, predict)

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
    score = model.score(Xtest,ytest)
    #print ("Getting predictions on train data...", time.ctime())    
    #predictionsTrain = model.predict(Xtrain)
    print ("Scoring check...", time.ctime())    
    check = model.score(Xtrain,ytrain)
    
    print("Done with all testing, saving outputs.", time.ctime())
    subfolder = util.string_appendDateAndTime(modelType) + '/'
    path = learn_util.makePathToTrajectories(filename) + subfolder
    if not os.path.exists(path):
        os.makedirs(path)  
    np.savetxt(path + 'ACTUALS-TEST.txt', ytest)
    np.savetxt(path + 'PREDICTIONS-TEST.txt', predictions)
    np.savetxt(path + 'SCORE-TEST.txt', np.array([score]))         
    #np.savetxt(path + 'ACTUALS-TRAIN.txt', ytrain)
    #np.savetxt(path + 'PREDICTIONS-TRAIN.txt', predictionsTrain)
    np.savetxt(path + 'SCORE-TRAIN.txt', np.array([check]))
    
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
svmR = svm.SVR(cache_size=2500) #default,
print("Fitting default model...", time.ctime())
svmR.fit(Xtrain,ytrain)
modelType = 'SVM-1-0.1'
if mean_centered==1:
    modelType = modelType + '-mean_centered'
saveModelStuff(svmR, modelType, Xtest, ytest, Xtrain, ytrain, filename)
for penalties in [0.1, 1]:
    for eps in [1, 0.1]:
        svmR = svm.SVR(C=penalties,epsilon=eps,cache_size=2500) #kernel='rbf',
        print("Fitting svm model...", time.ctime())
        svmR.fit(Xtrain,ytrain)
        model_type = 'SVM-'+str(penalties)+'-'+str(eps)
        if mean_centered==1:
            modelType = model_type + '-mean_centered'
        saveModelStuff(svmR, model_type , Xtest, ytest, Xtrain, ytrain, filename)

linmod1 = linear_model.LinearRegression() #aka least squares
print("Fitting linreg model...", time.ctime())
linmod1.fit(Xtrain, ytrain)
modelType = 'linReg'
if mean_centered==1:
    modelType = modelType + '-mean_centered'

saveModelStuff(linmod1, modelType, Xtest, ytest, Xtrain, ytrain, filename)
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