import pandas as pd
import numpy as np
import math
import re

# to check number of missing value
def noOfMissingValues(mergedData):
    count = 0
    colNumber = 0
    for colName in mergedData:
        if colNumber>=1:
            for i in range(mergedData[colName].shape[0]):
                if (mergedData[colName][i] == 'NR' or mergedData[colName][i] == '@' or math.isnan(float(mergedData[colName][i]))):
                    count = count + 1
        colNumber = colNumber + 1
    return count
# Function to fill missing values
def fillMissingValues(mergedData):
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

    return mergedData

# Start Merging

fname = "drop-out-rate"

df1 = pd.read_csv("datagov_new/Education/" + fname + ".csv")

grouped = df1.groupby('Year')
allGroups = []

for yearName,group in grouped:
    i = 0
    for colname in group.columns:
        if i > 1:
            group.rename(columns={colname: colname+"_"+yearName + "_" + fname + "_education"}, inplace=True)
        i = i + 1
    allGroups.append(group)
    
for i in range(len(allGroups)):
    allGroups[i] = allGroups[i].drop(['Year'], axis=1)


result = pd.merge(allGroups[0], allGroups[1], left_on=["State_UT"], right_on=["State_UT"], how="outer")
for i in range(2, len(allGroups)):
    result = pd.merge(result, allGroups[i], left_on=["State_UT"], right_on=["State_UT"], how="outer")
    

# print "till dropout", result.shape
files = ["gross-enrolment-ratio-higher-education", 
         "gross-enrolment-ratio-schools",
         "percentage-schools-boys-toilet",
         "percentage-schools-computers",
         "percentage-schools-drinking-water",
         "percentage-schools-electricity",
         "percentage-schools-girls-toilet"]
for fname in files:
    df1 = pd.read_csv("datagov_new/Education/" + fname + ".csv") 
    grouped = df1.groupby('Year')
    allGroups = []
    # print df1['Year'].value_counts()
    
    for yearName,group in grouped:
       
        i = 0
        for colname in group.columns:
            if i > 1:
                group.rename(columns={colname: colname+"_"+yearName + "_" + fname + "_education"}, inplace=True)
            i = i + 1
        
        allGroups.append(group)
        
    for i in range(len(allGroups)):
        allGroups[i] = allGroups[i].drop(['Year'], axis=1)
    
    
    for i in range(len(allGroups)):
        result = pd.merge(result, allGroups[i], left_on=["State_UT"], right_on=["State_UT"], how="outer")
    # print "till ", fname, result.shape


fname = "literacy-rate-7-years"
df1 = pd.read_csv("datagov_new/Education/" + fname + ".csv")
i = 0
for colname in df1.columns:
    if i > 0:
        df1.rename(columns={colname: colname+"_"+ fname + "_education"}, inplace=True)
    i = i + 1
result = pd.merge(result, df1, left_on=["State_UT"], right_on=["State_UT"], how="outer")

mergedDataEducation = result
print "Merged Data for Education Created"
mergedDataEducation = fillMissingValues(mergedDataEducation)
#print "No of missing values for final education data ====> ", noOfMissingValues(mergedDataEducation)
result.to_csv("finalDataEducation.csv", index = False)
print "Final Data for Education Created"
# print "till ", fname, result.shape

# Merging Demography folder
files = ["child-sex-ratio-0-6-years",
         "decadal-growth-rate",
         "sex-ratio"]
df1 = pd.read_csv("datagov_new/Demography/" + files[0] + ".csv")
df1 = df1.drop(['Category'], axis=1)
i = 0
for colname in df1.columns:
    if i > 0:
        df1.rename(columns={colname: colname+"_"+ files[0] + "_demography"}, inplace=True)
    i = i + 1
df2 = pd.read_csv("datagov_new/Demography/" + files[1] + ".csv")
df2 = df2.drop(['Category'], axis=1)
i = 0
for colname in df2.columns:
    if i > 0:
        df2.rename(columns={colname: colname+"_"+ files[1] + "_demography"}, inplace=True)
    i = i + 1
df3 = pd.read_csv("datagov_new/Demography/" + files[2] + ".csv")
df3 = df3.drop(['Category'], axis=1)
i = 0
for colname in df3.columns:
    if i > 0:
        df3.rename(columns={colname: colname+"_"+ files[2] + "_demography"}, inplace=True)
    i = i + 1

result = pd.merge(df1, df2, left_on=["State_UT"], right_on=["State_UT"], how="outer")

result = pd.merge(result, df3, left_on=["State_UT"], right_on=["State_UT"], how="outer")
mergedDataDemography = result
print "Merged Data for Demography Created"
mergedDataDemography = fillMissingValues(mergedDataDemography)
result.to_csv("finalDataDemography.csv", index = False)

# Merging Economy folder


fname = "gross-domestic-product-gdp-constant-price"
df1 = pd.read_csv("datagov_new/Economy/" + fname + ".csv")
df1["Items Description"] = df1["Items Description"].map(str) + "_" + df1["Duration"] + "_" + fname + "_economy"
df1 = df1.drop(['Duration'], axis=1)
df1 = df1.T
header = df1.iloc[0]
df1 = df1[1:]
df1.columns = header
i = 0
for colname in df1.columns:
    if i == 0:
        df1.rename(columns={colname:"State_UT"}, inplace=True)
    i = i + 1

fname = "gross-domestic-product-gdp-current-price"
df2 = pd.read_csv("datagov_new/Economy/" + fname + ".csv")
df2["Items Description"] = df2["Items Description"].map(str) + "_" + df2["Duration"] + "_" + fname + "_economy"
df2 = df2.drop(['Duration'], axis=1)
df2 = df2.T
header = df2.iloc[0]
df2 = df2[1:]
df2.columns = header
i = 0
for colname in df2.columns:
    if i == 0:
        df2.rename(columns={colname:"State_UT"}, inplace=True)
    i = i + 1
result = pd.merge(df1, df2, left_on=["State_UT"], right_on=["State_UT"], how="outer")

files = ["state-wise-net-domestic-product-ndp-constant-price",
         "state-wise-net-domestic-product-ndp-current-price"]

for fname in files:
    df1 = pd.read_csv("datagov_new/Economy/" + fname + ".csv")
    df1["Items Description"] = df1["Items Description"].map(str) + "_" + df1["Duration"] + "_" + fname + "_economy"
    df1 = df1.drop(['Duration'], axis=1)
    df1 = df1.T
    header = df1.iloc[0]
    df1 = df1[1:]
    df1.columns = header
    i = 0
    for colname in df1.columns:
        if i == 0:
            df1.rename(columns={colname:"State_UT"}, inplace=True)
        i = i + 1
    result = pd.merge(result, df1, left_on=["State_UT"], right_on=["State_UT"], how="outer")
    # print "till ", fname, result.shape


mergedDataEconomy = result
print "Merged Data for Economy Created"
mergedDataEconomy = fillMissingValues(mergedDataEconomy)
result.to_csv("finalDataEconomy.csv", index = False)
print "Final Data for Economy Created"

result = pd.merge(mergedDataEducation, mergedDataDemography, left_on=["State_UT"], right_on=["State_UT"], how="outer")
result = pd.merge(result, mergedDataEconomy, left_on=["State_UT"], right_on=["State_UT"], how="outer")
print "Final Data according to categories Created"
print "No of missing values for final education data ====> ", noOfMissingValues(mergedDataEducation)
print "No of missing values for final demography data ====> ", noOfMissingValues(mergedDataDemography)
print "No of missing values for final Economy data ====> ", noOfMissingValues(mergedDataEconomy)

print noOfMissingValues(result)
result = fillMissingValues(result)
print "No of missing values for final data ====> ", noOfMissingValues(mergedDataEconomy)
result.to_csv("finalDataCategories.csv", index = False)
