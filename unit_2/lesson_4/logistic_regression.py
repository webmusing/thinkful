import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

loansData = pd.read_csv('../resources/loansData_clean.csv')

#print loansData.head()

loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x >= 12 else 0 )

#print loansData.head()

print loansData[loansData['Interest.Rate'] == 10].head()
print loansData[loansData['Interest.Rate'] == 13].head()

loansData['intercept'] = 1.0

print loansData.head()

ind_vars = list(loansData.columns.values)

print ind_vars

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

result = logit.fit()

coeff = result.params
print(coeff)