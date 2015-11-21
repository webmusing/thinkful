"""
Challenge 1:
Write a script called "database.py" to print out the cities with the July being the warmest month. Your script must:

Connect to the database
Create the cities and weather tables (HINT: first pass the statement DROP TABLE IF EXISTS <table_name>; to remove the table before you execute the CREATE TABLE ... statement)
Insert data into the two tables
Join the data together
Load into a pandas DataFrame
Print out the resulting city and state in a full sentence. For example: "The cities that are warmest in July are: Las Vegas, NV, Atlanta, GA..."
Push your code to Github and enter the link below
Submit your code using the link below. If you have trouble, be sure to review the material in this lesson, search online resources, and reach out to your mentor. Good luck!

Challenge 2:
Try to write this script so the input can be more dynamic. 
Either take in the name of a month or have the user enter the value interactively. 
Query the database and return a result. 
Remember you'll have to handle all kinds of input. 
You take in command line input using the sys package. 
Don't spend too much time on this, especially if you've never programmed before. 
Dynamic input is one way to make code more functional but won't be a necessity going forward. 
You can find plenty of tutorials on how to accept user input online.
"""
import sys, traceback
import sqlite3 as lite
import numpy as py
import pandas as pd
from optparse import OptionParser

def get_options():
	month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

	parser = OptionParser()
	parser.add_option("-v", action="store_true", dest="verbose")
	parser.add_option("--month", type="string", dest="month", help="Input full month's name")

	parser.set_defaults(verbose=False,
		month=None)

	(options,args) = parser.parse_args()

	errors = list()

	if options.month is not None:
		if options.month not in month_list:
			errors.append("Invalid month input. Full month's name required.")

	if errors:
		parser.error("\n".join(errors))

	return (options, args)

def executeQuery(query, cnx, cmd):
	try:
		if cmd == "insert" or cmd == "update" or cmd == "drop" or cmd == "create":
			cursor = cnx.cursor()
			cursor.execute(query)
			cnx.commit()

		if cmd == "select":
			cursor = cnx.cursor()
			cursor.execute(query)
			return cursor.fetchall()
        
        #print cursor
	except Exception, msg:
		err = traceback.format_exc()
		print err
		print query

def createTables(cfg, cnx):
	# Processing cities table
	query = ("""DROP TABLE IF EXISTS `cities`;""")
	executeQuery(query, cnx, "drop")

	if cfg['verbose'] is True:
		print "Dropped table `cities`."

	query = ("""CREATE TABLE cities (name text, state text);""")
	executeQuery(query, cnx, "create")

	if cfg['verbose'] is True:
		print "Created table `cities`."

	# Processing weather table
	query = ("""DROP TABLE IF EXISTS `weather`;""")
	executeQuery(query, cnx, "drop")

	if cfg['verbose'] is True:
		print "Dropped table `weather`."

	query = ("""CREATE TABLE weather (city text, year int, warm_month text, cold_month text, average_high int);""")
	executeQuery(query, cnx, "create")

	if cfg['verbose'] is True:
		print "Created table `weather`."

def importData(cfg, cnx):
	query = ("""INSERT INTO cities (name, state) VALUES
		('New York City', 'NY'),
		('Boston', 'MA'),
		('Chicago', 'IL'),
		('Miami', 'FL'),
		('Dallas', 'TX'),
		('Seattle', 'WA'),
		('Portland', 'OR'),
		('San Francisco', 'CA'),
		('Los Angeles', 'CA');""")
	executeQuery(query, cnx, "insert")

	query = ("""INSERT INTO weather (city, year, warm_month, cold_month, average_high) VALUES
		('New York City', 2013, 'July', 'January', 62),
		('Boston', 2013, 'July', 'January', 59),
		('Chicago', 2013, 'July', 'January', 59),
		('Miami', 2013, 'August', 'January', 84),
		('Dallas', 2013, 'July', 'January', 77),
		('Seattle', 2013, 'July', 'January', 61),
		('Portland', 2013, 'July', 'December', 63),
		('San Francisco', 2013, 'September', 'December', 64),
		('Los Angeles', 2013, 'September', 'December', 75);""")
	executeQuery(query, cnx, "insert")

def getDataToDF(cfg, cnx):
	query = ("""SELECT name, state, year, warm_month, cold_month, average_high 
		FROM cities 
		INNER JOIN weather 
		ON name = city;""")

	df = pd.read_sql(query,con=cnx)
	return df

def printJulyWarmestCities(df, cfg, cnx):
	cities = df['name'][df.warm_month == 'July'].values.tolist()

	print "The cities that are warmest in July are: " + ", ".join(cities)

def customWarmestCities(df, cfg, cnx):
	cities = df['name'][df.warm_month == cfg['month']].values.tolist()

	print "User selected " + cfg['month'] + "."

	if not cities:
		print "There are no cities with the warmest month in " + cfg['month'] + "."
	else:
		print "The cities that are warmest in " + cfg['month'] + " are: " + ", ".join(cities)
def main():
	try:
		"""
		con = lite.connect('getting_started.db')

		with con:
			cur = con.cursor()
			cur.execute('SELECT SQLITE_VERSION()')
			data = cur.fetchone()

			print("SQLite version: %s" % data)

			cur.execute('SELECT * FROM cities;')
			rows = cur.fetchall()

			for row in rows:
				print row

			df = pd.DataFrame(rows)
		"""
		# Define config variable
		cfg = dict()

		# Get parameters from user-input
		options, args = get_options()
		cfg['verbose'] = options.verbose
		cfg['month'] = options.month

		# Creating connection
		cnx = lite.connect('getting_started.db')

		# Re-creating tables
		createTables(cfg, cnx)

		# Import data
		importData(cfg, cnx)

		# Join the 2 tables and input them into a dataframe
		df = getDataToDF(cfg, cnx)

		# Print cities with the warmest month in July
		printJulyWarmestCities(df, cfg, cnx)

		if cfg['month'] is not None:
			customWarmestCities(df, cfg, cnx)

	except Exception, msg:
		err = traceback.format_exc()

		print err

if __name__ == '__main__':
    main()