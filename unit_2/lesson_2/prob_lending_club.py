import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

loansData = pd.read_csv('../resources/loansData.csv')

loansData.dropna(inplace=True)

loansData.boxplot(column='Amount.Funded.By.Investors')

plt.show()

# Histogram Plot
loansData.hist(column='Amount.Funded.By.Investors')
plt.show()

plt.figure()

graph = stats.probplot(loansData['Amount.Funded.By.Investors'], dist="norm", plot=plt)

plt.show()

loansData.boxplot(column='Amount.Requested')

plt.show()

# Histogram Plot
loansData.hist(column='Amount.Requested')
plt.show()

plt.figure()

graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)

plt.show()