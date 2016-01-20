import pandas as pd
import numpy as np
# matplotlib 
import matplotlib as mpl
# matplotlib plotting functions
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 50, 50
import statsmodels.api as sm

df = pd.read_csv('../resources/LoanStats3b.csv', header=1, low_memory=False)

print df.columns.values

# converts string to datetime object in pandas:
df['issue_d_format'] = pd.to_datetime(df['issue_d']) 
dfts = df.set_index('issue_d_format') 
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

loan_count_summary.plot()

sm.graphics.tsa.plot_acf(loan_count_summary)

sm.graphics.tsa.plot_pacf(loan_count_summary)