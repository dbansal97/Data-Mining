import pandas as pd
import numpy as np
import math

# Start Merging

fname = "drop-out-rate"

df1 = pd.read_csv("datagov_new/Education/" + fname + ".csv")

grouped = df1.groupby('Year')
allGroups = []

for yearName,group in grouped:
    i = 0
    for colname in group.columns:
        if i > 1:
            group.rename(columns={colname: colname+"_"+yearName + "_" + fname}, inplace=True)
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
                group.rename(columns={colname: colname+"_"+yearName + "_" + fname}, inplace=True)
            i = i + 1
        
        allGroups.append(group)
        
    for i in range(len(allGroups)):
        allGroups[i] = allGroups[i].drop(['Year'], axis=1)
    
    
    for i in range(len(allGroups)):
        result = pd.merge(result, allGroups[i], left_on=["State_UT"], right_on=["State_UT"], how="outer")
    # print "till ", fname, result.shape


fname = "literacy-rate-7-years"
df1 = pd.read_csv("datagov_new/Education/" + fname + ".csv") 
result = pd.merge(result, df1, left_on=["State_UT"], right_on=["State_UT"], how="outer")
# print "till ", fname, result.shape

# Merging Demography folder into Education
files = ["child-sex-ratio-0-6-years",
         "decadal-growth-rate",
         "sex-ratio"]
for fname in files:
    df1 = pd.read_csv("datagov_new/Demography/" + fname + ".csv") 
    df1 = df1.drop(['Category'], axis=1)
    result = pd.merge(result, df1, left_on=["State_UT"], right_on=["State_UT"], how="outer")
    # print "till ", fname, result.shape

# Merging Economy folder in rest of data

files = ["gross-domestic-product-gdp-constant-price",
         "gross-domestic-product-gdp-current-price",
         "state-wise-net-domestic-product-ndp-constant-price",
         "state-wise-net-domestic-product-ndp-current-price"]

for fname in files:
    df1 = pd.read_csv("datagov_new/Economy/" + fname + ".csv")
    df1["Items Description"] = df1["Items Description"].map(str) + "_" + df1["Duration"] + "_" + fname
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



result.to_csv("mergedData.csv", index = False)
print "Merged Data Created"