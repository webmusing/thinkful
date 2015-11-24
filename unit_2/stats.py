import pandas as pd
from scipy import stats

data = '''Region,Alcohol,Tobacco
North,6.47,4.03
Yorkshire,6.13,3.76
Northeast,6.19,3.77
East Midlands,4.89,3.34
West Midlands,5.63,3.47
East Anglia,4.52,2.92
Southeast,5.89,3.20
Southwest,4.79,2.71
Wales,5.27,3.53
Scotland,6.08,4.51
Northern Ireland,4.02,4.56'''

# splitting into individual lines
data = data.splitlines()

data = [i.split(',') for i in data]

column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns=column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
alcohol_range = max(df['Alcohol']) - min(df['Alcohol'])
df['Tobacco'] = df['Tobacco'].astype(float)
tobacco_range = max(df['Tobacco']) - min(df['Tobacco'])

print "The range for the Alcohol and Tobacco dataset is " + str(alcohol_range) + " and " + str(tobacco_range) + " respectively."

print "The mean for the Alcohol and Tobacco dataset is " + str(df['Alcohol'].mean()) + " and " + str(df['Tobacco'].mean()) + " respectively."

print "The median for the Alcohol and Tobacco dataset is " + str(df['Alcohol'].median()) + " and " + str(df['Tobacco'].median()) + " respectively."

alcohol_mode = stats.mode(df['Alcohol'])
tobacco_mode = stats.mode(df['Tobacco'])
print "The mode for the Alcohol and Tobacco dataset is " + str(alcohol_mode[0]) + " and " + str(tobacco_mode[0]) + " respectively."

print "The variance for the Alcohol and Tobacco dataset is " + str(df['Alcohol'].var()) + " and " + str(df['Tobacco'].var()) + " respectively."

print "The standard deviation for the Alcohol and Tobacco dataset is " + str(df['Alcohol'].std()) + " and " + str(df['Tobacco'].std()) + " respectively."