from bs4 import BeautifulSoup
import requests, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
	list_headers = list()
	url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

	r = requests.get(url)

	soup = BeautifulSoup(r.content)

	#print type(soup)
	#print type(soup.find('tr', class_='lheader'))

	raw_headers = soup.find('tr', class_='lheader')

	#print raw_headers
	for tag in raw_headers('td'):
		#print tag.getText()
		list_headers.append(tag.getText())

	data_list = list() 
	#data_list.append(list_headers)

	for tag in raw_headers.find_next_siblings():
		row_list = list()
		for td in tag.find_all('td'):
			row_list.append(td.getText())
		data_list.append(row_list)

	tbl_df = pd.DataFrame(data_list)

	tbl_df[2] = np.nan
	tbl_df[3] = np.nan
	tbl_df[5] = np.nan
	tbl_df[6] = np.nan
	tbl_df[8] = np.nan
	tbl_df[9] = np.nan
	tbl_df[11] = np.nan
	tbl_df.dropna(axis=1,inplace=True)
	# Setting column headers for readability
	tbl_df.columns = ['Country_Area','Year','Total','Men','Women']

	tbl_df['Year'] = pd.to_datetime(tbl_df['Year'], format='%Y')

	tbl_df[['Total','Men','Women']] = tbl_df[['Total','Men','Women']].fillna(0).astype(int)
	
	plt.figure()
	tbl_df.boxplot()
	plt.show()
	
	
if __name__ == '__main__':
	main()
