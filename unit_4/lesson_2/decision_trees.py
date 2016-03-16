#!/usr/bin/env python
from datetime import tzinfo, timedelta, datetime
import time, pytz
import traceback,logging,os,signal,time,gzip,StringIO,logging.handlers,re,sys,requests, mysql.connector
import numpy as np
import pandas as pd

def cleanData(config):
	#with open(config['uci_column_names'],'rU') as f:
		#print f.readlines().strip()

	uci_column_names = set(line.split(" ")[1].replace("()","").replace("BodyBody","").replace("Body","").replace("Mag","").strip() for line in open(config['uci_column_names']))
	uci_column_names = set(re.sub("-[0-9]-[0-9]","",re.sub("-[0-9][0-9],[0-9][0-9]", "", line)) for line in uci_column_names)
	uci_column_names = set(re.sub(",\d","",re.sub("-[0-9]-[0-9][0-9]","",line)) for line in uci_column_names)
	uci_column_names = set(re.sub("\),", ",", line) for line in uci_column_names)
	print uci_column_names
	print len(uci_column_names)
	
def main():
	config = dict()
	config['resource_dir'] = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../')) + "/resources/"
	config['uci_activity_labels'] = config['resource_dir'] + "UCI_HAR_Dataset/activity_labels.txt"
	config['uci_column_names'] = config['resource_dir'] + "UCI_HAR_Dataset/features.txt"
	config['uci_test_dir'] = config['resource_dir'] + "UCI_HAR_Dataset/test/"
	config['uci_train_dir'] = config['resource_dir'] + "UCI_HAR_Dataset/train/"
	
	cleanData(config)
	#print config

if __name__ == '__main__':
	main()