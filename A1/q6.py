import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.spatial import distance
from sklearn import preprocessing
import random
import sys
import scipy.stats as stats
import pylab 
import statsmodels.api as sm
from math import log10, floor

# stores the regions of states
regionsData = pd.read_csv('regions.csv')
regionsData = regionsData.values
regions = {}
for row in regionsData:
    regions[row[0]] = row[1]
    


# Normalizing (Min-max normalization with range(0-1))
def normalizeTheData(finalData):
    df = finalData.loc[:]
    i = 0
    for col in df.columns:
        if not(i == 0):
            df[col] = (df[col]-df[col].min())/(df[col].max()-df[col].min())
        i = i + 1
    return df

def findNearestDistances(index, finalData, shift=0):
    tmp = finalData.loc[:, finalData.columns != 'State_UT']
    states = finalData['State_UT']
    vectorOfRandomObject = tmp.iloc[index]
     
    distances = {}
    for i in range(tmp.shape[0]):
        if not(i == index or i==shift):
            row = tmp.iloc[i]
            distances[i] = distance.euclidean(row,vectorOfRandomObject)
    
    #print states[index], regions[states[index]]
    nearestHitDistance = sys.maxint
    hitIndex = index
    missIndex = index
    nearestMissDistance = sys.maxint
    for key in distances.keys():
        if regions[states[key]] == regions[states[index]]:
            if nearestHitDistance > distances[key]:
                nearestHitDistance = distances[key]
                hitIndex = key
        else:
            if nearestMissDistance > distances[key]:
                nearestMissDistance = distances[key]
                missIndex = key
    #print states[hitIndex], states[missIndex]
    return tmp.iloc[hitIndex], tmp.iloc[missIndex]
   
    
def reliefAlgorithm(finalData, shift, numOfTimes = 30):
    
    finalData.sort_values(by=['State_UT'])
    
    finalData = normalizeTheData(finalData)
    states = finalData['State_UT']
    scores = np.zeros(finalData.shape[1]-1)
    
    for i in range(numOfTimes):
        if shift == 0: # Demography
            randomObjectIndex = random.randint(1, finalData.shape[0]-1)
        elif shift == 33: # Economy
            randomObjectIndex = random.randint(0, finalData.shape[0]-2)
        elif shift == 35: # Education:
            randomObjectIndex = random.randint(0, finalData.shape[0]-1)
            if randomObjectIndex == 35:
                randomObjectIndex = randomObjectIndex = random.randint(0, finalData.shape[0]-3)
        nearestHitVector, nearestMissVector = findNearestDistances(randomObjectIndex, finalData, shift)
        scores = scores - nearestHitVector + nearestMissVector
        #print scores
    return scores


fnames = ['finalDataDemography', 'finalDataEconomy', 'finalDataEducation', 'finalDataCategories']
shifts = [0, 33, 35, 35]
 

i = 0
for fname in fnames:
    finalData = pd.read_csv(fname + ".csv")
    scores = reliefAlgorithm(finalData, shifts[i], 1000)
    scores = scores.sort_values()
    #print "\nFor", fname, "\n-------------------------------\n"
    first = scores.idxmax()
    #print "Most Important Attribute =>", scores.idxmax()
    scores[scores.idxmax()] = -sys.maxint-1
    #print "Second Most Important Attribute =>", scores.idxmax()
    second = scores.idxmax()
    X = finalData[first]
    Y = finalData[second]
    X = X.sort_values()
    Y = Y.sort_values()
    
    outputFile = open(fname + "_q6_input.txt","w+")
    answer = ""

   
    outputFile.write("For " + fname + "\nX => ")
    for x in X:
        outputFile.write(str(x)+" ")
    outputFile.write("\n5% Quantile - " + str(X.quantile(0.05)) + "\n")
    outputFile.write("95% Quantile - " + str(X.quantile(0.95)) + "\n")

    outputFile.write("Y => ")
    for y in Y:
        outputFile.write(str(y)+" ")
    outputFile.write("\n5% Quantile - " + str(Y.quantile(0.05)) + "\n")
    outputFile.write("95% Quantile - " + str(Y.quantile(0.95)) + "\n")
    outputFile.close()
    print "Done for", fname