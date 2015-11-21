import collections
import json
import numpy as np
import pandas as pd

population_dict = collections.defaultdict(int)
with open('lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_continent-90m.csv','rU') as inputFile:
    header = next(inputFile)
    for line in inputFile:
        line = line.rstrip().split(',')
        line[5] = int(line[5])
        if line[1] == 'Total National Population':
            population_dict[line[0]] += line[5]

print json.dumps(population_dict, sort_keys=False, indent=2, separators=(',', ': '))

with open('national_population.csv', 'w') as outputFile:
    outputFile.write('continent,2010_population\n')

    for k, v in population_dict.iteritems():
        outputFile.write(k + ',' + str(v) + '\n')

"""
Challenge 1.
The data world is now your oyster. 
Play with some of the other population data and see what you come up with. 
Try and calculate the population change between 2010 and 2100. 
Remember the lesson about doing integer division. 
Convert one of the numbers to floating point decimal by using the float() function. 
Which continent is estimated to grow the most in the next 90 years?

Challenge 2.
Try and calculate the population density (total national population divided by the total land area and remember to convert at least one number to float). 
Which continent was most densely populated in 2010?
"""

continent_df = pd.read_csv("lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_continent-90m.csv")

# Calculate different between Population2100 and Population2010
continent_df['Diff_2010_2100'] = continent_df['Population2100'] - continent_df['Population2010']

# Change the difference to float
continent_df['Diff_2010_2100'] = continent_df['Diff_2010_2100'].astype(float)

# Add population density
continent_df['population_density_2010'] = continent_df['Population2010']/continent_df['LandArea']

# Group by continent for population, difference and its density
print continent_df.groupby('Continent').agg({'Population2010':np.sum,'Population2100':np.sum,'LandArea':np.sum,'Diff_2010_2100':np.sum, 'population_density_2010':np.sum})
print "\n"

# Answers for challenge
print "Answers for challenge:"
print continent_df.groupby('Continent').agg({'Diff_2010_2100':np.sum,'population_density_2010':np.sum}).idxmax()