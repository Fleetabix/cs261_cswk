import feedparser
import datetime
import pandas_datareader.data as web
import requests
import datatime

class CompanyStock:
	def __init__(self, spotprice, change, percentchange, retrieve_datetime):
		self.spot_price = spotprice
		self.price_difference = change
		self.percent_difference = percentchange
		self.retrieved = retrieve_datetime

def getStockInformation(ticker): 
	# [possibly] Temporary rss feed for now - till better one is found - current implementation is slow
	response = requests.get('http://m.londonstockexchange.com/exchange/mobile/stocks/summary.html?tidm='+ticker)
	cs = None
	if (response.status_code == 200):
		soup = bs4.BeautifulSoup(response.content, "lxml")
		data = soup.find("div", {"class": "tr darkEven"})
		stock = [x.text.strip() for x in data.findAll('span')]
		retrieved = datetime.datetime.now()-datetime.timedelta(minutes=15)
		cs = CompanyStock(stock[0], stock[1], stock[2], retrieved)
	return cs
def getHistoricalStockInformation(ticker, start, end):
	data = web.DataReader(ticker, "google", start, end)
	return data
		
