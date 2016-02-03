import pandas as pd

df = pd.DataFrame({'rainy':[.4, .7], 'sunny':[.6,.3]}, index=['rainy','sunny'])

print df.dot(df)