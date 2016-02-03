import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

loansData = pd.read_csv('../resources/loansData_clean.csv')

#print loansData.head()
#print loansData.dtypes

loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x >= 12 else 0 )
#print loansData[['Interest.Rate','IR_TF']].head()
#print loansData.head()

#print loansData[loansData['Interest.Rate'] == 10].head()
#print loansData[loansData['Interest.Rate'] > 12].head()

# Statsmodels needs an intercept column in your dataframe, so add a column with a constant intercept of 1.0.
loansData['intercept'] = 1.0

#print loansData.head()

#ind_vars = list(loansData.columns.values)
#print ind_vars
#ind_vars_df = loanData.loc[:, ('column1', 'column2')]  # create separate df

ind_vars = ['Amount.Requested', 'Loan.Length', 'FICO.Range', 'intercept']

print loansData.dtypes

print loansData.head()

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

result = logit.fit()

coeff = result.params
print(coeff)