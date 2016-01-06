import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('../resources/loansData.csv')

print loansData['Interest.Rate'][0:5]

print loansData['Loan.Length'][0:5]

print loansData['FICO.Range'][0:5]

# Remove % symbol
#print "Removed symbol"
interest_rate = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%'))/100,4))
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%'))/100,4)) * 100
#print interest_rate[0:5]

# Remove months
#print "Removed months"
loan_length = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
#print loan_length[0:5]

# Remove dashes into tuple or list
fico_range = loansData['FICO.Range'].map(lambda x: x.split('-'))
#print fico_range[0:5]
fico_score = fico_range.map(lambda x: x[0]).astype(int)
loansData['FICO.Range'] = fico_range.map(lambda x: x[0]).astype(int)
#print fico_score[0:5]

print loansData.head()

# Plot Histogram of FICO score
plt.figure()
p=fico_score.hist()
plt.show()

# scatter plot
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
print a

y = np.matrix(interest_rate).transpose()
x1 = np.matrix(fico_score).transpose()
x2 = np.matrix(loan_length).transpose()

x = np.column_stack([x1,x2])

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

print f.summary()

loansData.to_csv('../resources/loansData_clean.csv', header=True, index=False)