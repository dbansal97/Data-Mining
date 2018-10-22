import pandas as pd
import numpy as np
import math
import re
import matplotlib.pyplot as plt

files = [ "finalDataEconomy", "finalDataCategories", "finalDataDemography", "finalDataEducation"]

for fname in files:
    outputFile = open(fname + "_CorrOutput.txt","w+")
    answer = ""

    df= pd.read_csv(fname + '.csv')
    df.sort_values(by=['State_UT'])
     
    
    ans = df.corr(method='kendall')
    allColumns = ans.columns
    print type(ans)
    # Negatively Correlated
    for col in ans.columns:
        for i in range(ans[col].shape[0]):
            if ans[col][i] < 0:
                answer = answer + "=> " + col + " <= and => " + allColumns[i] + " <= are negatively correlated\n"
    answer = answer + "\n<============================================>\n\n"
    # Highly Correlated
    for col in ans.columns:
        for i in range(ans[col].shape[0]):
            if ans[col][i] > 0.95 and not(ans[col][i]==1):
                answer = answer + "=> " + col + " <= and => " + allColumns[i] + " <= are highly correlated\n"
    answer = answer + "\n<============================================>\n\n"
    # Nearly independent 
    for col in ans.columns:
        for i in range(ans[col].shape[0]):
            if ans[col][i] < 0.05:
                answer = answer + "=> " + col + " <= and => " + allColumns[i] + " <= are independent\n"
    outputFile.write(answer)
    outputFile.close()