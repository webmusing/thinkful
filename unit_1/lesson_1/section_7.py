import numpy as np
import pandas as pd
import os

urban_df = pd.read_csv("lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_codebook.csv")

print "Printing out the dataframe data:"
print urban_df

for i, val in urban_df.iterrows():
	print len(val)