#!/usr/bin/env python
import traceback,logging,os,signal,time,gzip,StringIO,logging.handlers,re,sys,requests, mysql.connector, json
import ftplib
from datetime import tzinfo, timedelta, datetime
from pandas.io.json import json_normalize

import matplotlib.pyplot as plt
import pandas as pd

from dateutil.parser import parse

import collections

import sqlite3 as lite

from optparse import OptionParser

def get_options():
	# Today's datetime
	today = dict()
	today['datetime'] = datetime.now()
	today['api_date'] = today['datetime'].strftime('%Y%m%d')

	#yesterday's datetime
	yesterday = dict()
	yesterday['datetime'] = datetime.now() - timedelta(days=1)
	yesterday['api_date'] = yesterday['datetime'].strftime('%Y%m%d')

	# Get command-line options
	parser = OptionParser()
	parser.add_option("-v", action="store_true", dest="verbose")
	parser.add_option("-q", action="store_false", dest="verbose")
	parser.add_option("--runSim", action="store_true", dest="run_sim")

	parser.set_defaults(verbose=False,
		run_sim=False)

	(options, args) = parser.parse_args()

	# Create an error list to identify errors
	errors = list()

	if errors:
	    parser.error("\n".join(errors))

	return (options,args)

def keywithmaxval(d):
    """Find the key with the greatest value"""
    return max(d, key=lambda k: d[k])

def reportBikes(con, cur):
	df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

	hour_change = collections.defaultdict(int)
	for col in df.columns:
	    station_vals = df[col].tolist()
	    station_id = col[1:] #trim the "_"
	    station_change = 0
	    for k,v in enumerate(station_vals):
	        if k < len(station_vals) - 1:
	            station_change += abs(station_vals[k] - station_vals[k+1])
	    hour_change[int(station_id)] = station_change #convert the station id back to integer

    # assign the max key to max_station
	max_station = keywithmaxval(hour_change)

	cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_ref WHERE id = ?", (max_station,))
	data = cur.fetchone()
	print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
	print("With %d bicycles coming and going in the hour between %s and %s" % (
	    hour_change[max_station],
	    datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
	    datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
	))

	plt.bar(hour_change.keys(), hour_change.values())
	plt.show()

def availableBikes(con, cur):
	r = requests.get('http://www.citibikenyc.com/stations/json')

	df = json_normalize(r.json()['stationBeanList'])

	df['availableBikes'].hist()
	#plt.show()

	df['totalDocks'].hist()
	#plt.show()

	# checking if there are multiple statusValues and statusKeys
	print df[['statusValue','statusKey']].drop_duplicates()

	# checking the types
	print df.dtypes

	# total in-service stations
	total_in_service = len(df[df.statusKey == 1])
	print "total in-service stations: " + str(total_in_service)

	# total not-in-service stations
	total_not_in_service = len(df[df.statusKey == 3])
	print "total not-in-service stations: " + str(total_not_in_service)

	# mean available bikes
	print "availableBikes mean: " + str(df['availableBikes'].mean())

	# median available bikes
	print "availableBikes median: " + str(df['availableBikes'].median())

	# Does the mean and the number of bikes change in a dock if we remove the stations that aren't in service?
	print str(df[df.statusKey == 3]['availableBikes'])
	# It does not change because the available bikes account to 0 when the dock is not in service.
	with con:

		query = ("""CREATE TABLE IF NOT EXISTS citibike_ref (
	    id INT PRIMARY KEY,
	    totalDocks INT,
	    city TEXT,
	    altitude INT, 
	    stAddress2 TEXT,
	    longitude NUMERIC,
	    postalCode TEXT,
	    testStation TEXT,
	    stAddress1 TEXT,
	    stationName TEXT,
	    landMark TEXT,
	    latitude NUMERIC,
	    location TEXT
		)""")

		cur.execute(query)

		for s in r.json()['stationBeanList']:
			query = ("""INSERT OR REPLACE INTO citibike_ref (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) 
			    VALUES 
			    ('{id}', '{totalDocks}', '{city}', '{altitude}', '{stAddress2}', '{longitude}', '{postalCode}', '{testStation}', '{stAddress1}', 
			    	'{stationName}', '{landMark}', '{latitude}', '{location}');
				""".format(id=s['id'], totalDocks=s['totalDocks'], city=s['city'], altitude=s['altitude'], stAddress2=s['stAddress2'], longitude=s['longitude'], postalCode=s['postalCode'], testStation=s['testStation'], stAddress1=s['stAddress1'], stationName=s['stationName'], landMark=s['landMark'], latitude=s['latitude'], location=s['location']))
			cur.execute(query)


	#extract the column from the DataFrame and put them into a list
	station_ids = df['id'].tolist() 

	#add the '_' to the station name and also add the data type for SQLite
	station_ids = ['_' + str(x) + ' INT' for x in station_ids]

	#create the table
	#in this case, we're concatenating the string and joining all the station ids (now with '_' and 'INT' added)
	with con:
		cur.execute("CREATE TABLE IF NOT EXISTS available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")


	exec_time = parse(r.json()['executionTime'])

	with con:
		cur.execute('INSERT OR REPLACE INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

	id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

	#loop through the stations in the station list
	for station in r.json()['stationBeanList']:
		id_bikes[station['id']] = station['availableBikes']

	#iterate through the defaultdict to update the values in the database
	with con:
		for k, v in id_bikes.iteritems():
			cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")

def main():
	try:
		config = dict()
		options, args = get_options()
		config['run_sim'] = options.run_sim

		con=lite.connect('citibike.db')
		cur = con.cursor()

		if config['run_sim'] == True:
			for i in range(60):
				availableBikes(con, cur)
				time.sleep(60)
		else:
			report(con,cur)

		con.close()
	except Exception, msg:
		err = traceback.format_exc()

		print err

if __name__ == '__main__':
	main()

