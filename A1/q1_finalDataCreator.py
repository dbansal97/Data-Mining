import pandas as pd
import numpy as np
import math
import re

mergedData = pd.read_csv('mergedData.csv')
mergedData.sort_values(by=['State_UT'])

# to check number of missing value
def noOfMissingValues():
    count = 0
    colNumber = 0
    for colName in mergedData:
        if colNumber>=1:
            for i in range(mergedData[colName].shape[0]):
                if (mergedData[colName][i] == 'NR' or mergedData[colName][i] == '@' or math.isnan(float(mergedData[colName][i]))):
                    count = count + 1
        colNumber = colNumber + 1
    return count

# stores the regions of states
regionsData = pd.read_csv('regions.csv')
regionsData = regionsData.values
regions = {}
for row in regionsData:
    regions[row[0]] = row[1]
    
states = mergedData['State_UT']

print "initial missing", noOfMissingValues()

# Filling the missing values which can be found using average of classes
colNumber = 0
for colName in mergedData:
    if colNumber>=1:
        regionStateSum = {}
        regionStateCount = {}
        for i in range(mergedData[colName].shape[0]):
            if regions[states[i]] in regionStateSum.keys():
                if not(mergedData[colName][i] == 'NR' or mergedData[colName][i] == '@' or math.isnan(float(mergedData[colName][i]))):
                    regionStateSum[regions[states[i]]] = regionStateSum[regions[states[i]]] + float(mergedData[colName][i])
                    regionStateCount[regions[states[i]]] = regionStateCount[regions[states[i]]] + 1
            else:
                if not(mergedData[colName][i] == 'NR' or mergedData[colName][i] == '@' or math.isnan(float(mergedData[colName][i]))):
                    regionStateSum[regions[states[i]]] = float(mergedData[colName][i])
                    regionStateCount[regions[states[i]]] = 1
        
        for key in regionStateSum.keys():
			regionStateSum[key] = regionStateSum[key]/regionStateCount[key]
        
        for i in range(mergedData[colName].shape[0]):
            if (mergedData[colName][i] == 'NR' or mergedData[colName][i] == '@' or math.isnan(float(mergedData[colName][i]))):
                if regions[states[i]] in regionStateSum.keys():
                    mergedData[colName][i] = regionStateSum[regions[states[i]]]
                else:
                    mergedData[colName][i] = float('nan')
    colNumber = colNumber + 1


print "missing after averaging", noOfMissingValues()

# Case where average of class is itself null

colNumber = 0
for colName in mergedData:
    if colNumber>=1:
        for i in range(mergedData[colName].shape[0]):
            if (mergedData[colName][i] == 'NR' or mergedData[colName][i] == '@' or math.isnan(float(mergedData[colName][i]))):
                allYears = ["2010-11","2011-12", "2012-13", "2013-14", "2014-15", "2015-16"]
                for year in allYears:
                    newColName = re.sub("[0-9-]*-[0-9]+", year, colName)
                    if newColName in mergedData.columns:
                        #print "newCol is amoung columns", colName, " ==>", newColName
                        if not(mergedData[newColName][i] == 'NR' or mergedData[newColName][i] == '@' or math.isnan(float(mergedData[newColName][i]))):
                            #print "replaced"
                            mergedData[colName][i] = mergedData[newColName][i]
                            break
        #if colNumber%10==0:
            #print "colNumber = ", colNumber

    colNumber = colNumber + 1
    

print "missing after assigning random year value", noOfMissingValues()

mergedData.to_csv("finalData.csv", index = False)
print "Final DataSet Created"