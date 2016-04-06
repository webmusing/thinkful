#!/usr/bin/env python
from datetime import tzinfo, timedelta, datetime
import time, pytz
import traceback,logging,os,signal,time,gzip,StringIO,logging.handlers,re,sys,requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier


def main():
	config = dict()
	config['resource_dir'] = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../')) + "/resources/"
	config['uci_activity_labels'] = config['resource_dir'] + "UCI_HAR_Dataset/activity_labels.txt"
	config['uci_column_names'] = config['resource_dir'] + "UCI_HAR_Dataset/features.txt"
	config['uci_test_dir'] = config['resource_dir'] + "UCI_HAR_Dataset/test/"
	config['uci_train_dir'] = config['resource_dir'] + "UCI_HAR_Dataset/train/"
	config['test_x_test'] = config['uci_test_dir'] + "X_test.txt"
	config['test_y_test'] = config['uci_test_dir'] + "Y_test.txt"
	config['train_x_train'] = config['uci_train_dir'] + "X_train.txt"
	config['train_y_train'] = config['uci_train_dir'] + "Y_train.txt"
	config['features'] = config['resource_dir'] + "UCI_HAR_Dataset/features.txt"

	activity_labels_df = pd.read_csv(config['uci_activity_labels'], sep=r"\s+", header=None).set_index(0)

	# Initialising train Y data set
	train_y_df = pd.read_csv(config['train_y_train'], header=None)
	train_y_df.columns=['activity_idx']
	train_y_df['activity_labels'] = train_y_df['activity_idx'].map(lambda x: activity_labels_df.loc[x].values[0])

	# Initialising test Y data set
	test_y_df = pd.read_csv(config['test_y_test'], header=None)
	test_y_df.columns=['activity_idx']
	test_y_df['activity_labels'] = test_y_df['activity_idx'].map(lambda x: activity_labels_df.loc[x].values[0])


	# Initialising headers
	col_headers_list = [line.split(" ")[1].strip() for line in open(config['features'])]
	col_headers_set = set(line.split(" ")[1].strip() for line in open(config['features']))

	# Initialising train X data set
	train_x_df = pd.read_csv(config['train_x_train'], sep=r"\s+",header=None)
	train_x_df.columns = col_headers_list

	train_x_df = pd.concat([train_x_df,train_y_df], axis=1)

	train_x_df = train_x_df.T.reset_index().drop_duplicates(subset='index',take_last=True).set_index('index').T
	train_x_df.rename(columns=lambda x: x.replace("BodyBody",""), inplace=True)
	train_x_df.rename(columns=lambda x: x.replace("Body",""), inplace=True)

	# Initialising test X data set

	test_x_df = pd.read_csv(config['test_x_test'], sep=r"\s+", header=None)
	test_x_df.columns = col_headers_list

	test_x_df = pd.concat([test_x_df,test_y_df], axis=1)

	test_x_df = test_x_df.T.reset_index().drop_duplicates(subset='index',take_last=True).set_index('index').T
	test_x_df.rename(columns=lambda x: x.replace("BodyBody",""), inplace=True)
	test_x_df.rename(columns=lambda x: x.replace("Body",""), inplace=True)
	#test_x_df.rename(columns=lambda x: x.replace("Mag",""), inplace=True)
	#test_x_df.columns.values.tolist()

	n_estimators = 10

	forest = RandomForestClassifier(n_estimators=n_estimators)

	forest = forest.fit(train_x_df[train_x_df.columns[0:-2]],train_x_df['activity_labels'])

	forest.estimators_
	importances = forest.feature_importances_

	plot_df = pd.DataFrame(train_x_df.columns[0:-2].values,columns=['feature'])
	plot_df['importance'] = forest.feature_importances_

	plot_df.sort_index(by='importance', ascending=False, inplace=True)

	plot_df.head(20).set_index('feature').plot(kind='barh')

	rslt = forest.predict(test_x_df[test_x_df.columns[0:-2]].values)

	print rslt




if __name__ == '__main__':
	main()