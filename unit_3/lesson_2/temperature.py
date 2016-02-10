import traceback,requests, json
import sqlite3 as lite
from datetime import tzinfo, timedelta, datetime

def main():
	try:
		config = dict()
		config['api_key'] = "b426cced70c6f01014857019e840bf8a"
		config['url'] = 'https://api.forecast.io/forecast/' + config['api_key'] + "/"
		config['end_date'] = datetime.now()

		con = lite.connect('weather.db')
		cur = con.cursor()

		cities = { "Atlanta": '33.762909,-84.422675',
			"Austin": '30.303936,-97.754355',
			"Boston": '42.331960,-71.020173',
			"Chicago": '41.837551,-87.681844',
			"Cleveland": '41.478462,-81.679435'
		}

		#print cities.keys()
		cities_key = (" REAL, ").join(cities.keys()) + " REAL"
		#print cities_key + " REAL"
		with con:
			query = ("""CREATE TABLE IF NOT EXISTS daily_temp ( day_of_reading INT, {cities_key});""".format(cities_key=cities_key))
			cur.execute(query)

		query_date = config['end_date'] - timedelta(days=30) #the current value being processed

		with con:
			while query_date < config['end_date']:
				cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
				query_date += timedelta(days=1)
		
		for k, v in cities.iteritems():
			
			#print k, v
			
			query_date = config['end_date'] - timedelta(days=30) #set value each time through the loop of cities
			while query_date < config['end_date']:
				#query for the value
				url_query = config['url'] + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00')
				#print url_query
				r = requests.get(config['url'] + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))

				with con:
				    #insert the temperature max to the database
				    if r.status_code == 200:
					    cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

				#increment query_date to the next day for next operation of loop
				query_date += timedelta(days=1) #increment query_date to the next day
				


	except Exception, msg:
		err = traceback.format_exc()

		print err

if __name__ == '__main__':
	main()
