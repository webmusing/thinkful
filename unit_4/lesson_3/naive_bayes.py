#!/usr/bin/env python
from datetime import tzinfo, timedelta, datetime
import time, pytz
import traceback,logging,os,signal,time,gzip,StringIO,logging.handlers,re,sys,requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB

def main():
	config = dict()
	config['resource_dir'] = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../')) + "/resources/"
	config['raw_file'] = config['resource_dir'] + "ideal_weight.csv"
	ideal_weight_df = None

	ideal_weight_df = pd.read_csv(config['raw_file'])
	ideal_weight_df.columns = [x.replace("\'","") for x in ideal_weight_df.columns.values.tolist()]
	
	ideal_weight_df.loc[:,'sex'] = ideal_weight_df['sex'].map(lambda x: x.replace("\'",""))
	#print ideal_weight_df
	#print config

	plt.hist(ideal_weight_df['actual'], alpha=0.5, label='actual')
	plt.hist(ideal_weight_df['ideal'], alpha=0.5, label='ideal')
	plt.show() # figure_1.png

	ideal_weight_df['diff'].hist()

	ideal_weight_df['sex_id'] = ideal_weight_df['sex'].map(lambda x: 1 if x == 'Male' else 0)

	clf = GaussianNB()
	clf.fit(ideal_weight_df[['actual','ideal','diff']],ideal_weight_df['sex'])

	print clf.predict([[145,160,-15]]) # male

	print clf.predict([[160,145,15]]) # female

if __name__ == '__main__':
	main()