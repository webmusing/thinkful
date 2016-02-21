from bs4 import BeautifulSoup
import requests, json
import pandas as pd

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

	#print data_list

	tbl_df = pd.DataFrame(data_list)
	print list_headers
	#print tbl_df.columns.values.tolist()
	#print tbl_df

	tbl_df.dropna(axis=1,how='all',inplace=True)
	#print tbl_df
	#print list_headers
	print tbl_df.columns.values.tolist()
	#print tbl_df['Men']
	
if __name__ == '__main__':
	main()
