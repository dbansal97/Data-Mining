import pandas as pd
import numpy as np
import math
import re
from scipy.spatial import distance
from sklearn import preprocessing


finalData = pd.read_csv('finalData.csv')
finalData.sort_values(by=['State_UT'])

# Without normailzing data

print "Without Normalized Representative States\n"
vectorOfIndia = finalData.loc[35]
vectorOfIndia = vectorOfIndia.values
vectorOfIndia = vectorOfIndia[1:]
vectorOfIndia = np.array(vectorOfIndia)


distances = {}
indexToStateName = {}
for i in range(finalData.shape[0]):
    if not(i == 35):
        row = finalData.loc[i]
        row = row.values
        stateName = row[0]
        indexToStateName[i] = stateName
        distances[stateName] = 0
        row = row[1:]
        row = np.array(row)
        distances[stateName] = distance.euclidean(row,vectorOfIndia)

topHowMany = 5        
for key, value in sorted(distances.iteritems(), key=lambda (k,v): (v,k)):
    if topHowMany > 0:
        print "%s: %s" % (key, value)
    topHowMany = topHowMany - 1

# With Normalizing (L2)
tmp = finalData.loc[:, finalData.columns != 'State_UT']
normalizedData = preprocessing.normalize(tmp, axis=0)
vectorOfIndia = normalizedData[35]
print "\nNormalized Representative States\n"
distancesNormalized = {}
for i in range(normalizedData.shape[0]):
    if not(i == 35):
        row = normalizedData[i]
        distancesNormalized[indexToStateName[i]] = distance.euclidean(row,vectorOfIndia)

topHowMany = 5        
for key, value in sorted(distancesNormalized.iteritems(), key=lambda (k,v): (v,k)):
    if topHowMany > 0:
        print "%s: %s" % (key, value)
    topHowMany = topHowMany - 1

# With Normalizing (Z-Score normalization)

df = finalData.loc[:, finalData.columns != 'State_UT']

i = 0
for col in df.columns:
   df[col] = (df[col]-df[col].mean())/df[col].std(ddof=0)

df = np.asarray(df)
vectorOfIndia = df[35]
print "\nNormalized Representative States with Z-Score Normailzation\n"
distancesZScoreNormalized = {}
for i in range(df.shape[0]):
    if not(i == 35):
        row = df[i]
        distancesZScoreNormalized[indexToStateName[i]] = distance.euclidean(row,vectorOfIndia)

topHowMany = 5        
for key, value in sorted(distancesZScoreNormalized.iteritems(), key=lambda (k,v): (v,k)):
    if topHowMany > 0:
        print "%s: %s" % (key, value)
    topHowMany = topHowMany - 1

# With Normalizing (Min-max normalization with range(0-1))

df = finalData.loc[:, finalData.columns != 'State_UT']

i = 0
for col in df.columns:
   df[col] = (df[col]-df[col].min())/(df[col].max()-df[col].min())

df = np.asarray(df)
vectorOfIndia = df[35]
print "\nNormalized Representative States with Min-Max Normailzation with range(0-1)\n"
distancesZScoreNormalized = {}
for i in range(df.shape[0]):
    if not(i == 35):
        row = df[i]
        distancesZScoreNormalized[indexToStateName[i]] = distance.euclidean(row,vectorOfIndia)

topHowMany = 5        
for key, value in sorted(distancesZScoreNormalized.iteritems(), key=lambda (k,v): (v,k)):
    if topHowMany > 0:
        print "%s: %s" % (key, value)
    topHowMany = topHowMany - 1