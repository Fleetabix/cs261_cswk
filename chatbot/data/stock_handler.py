import feedparser
import datetime
import pandas_datareader.data as web
import requests
import datetime
import bs4

class CompanyStock:
	def __init__(self, spotprice, change, percentchange, retrieve_datetime):
		self.spot_price = spotprice
		self.price_difference = change
		self.percent_difference = percentchange
		self.retrieved = retrieve_datetime

def getStockInformation(ticker): 
	response = requests.get('http://m.londonstockexchange.com/exchange/mobile/stocks/summary.html?tidm='+ticker)
	cs = None
	if (response.status_code == 200):
		soup = bs4.BeautifulSoup(response.content, "lxml")
		data = soup.find("div", {"class": "tr darkEven"})
		# Catches cases where the website redirects to homepage due to nonexistent company
		if data is None:
			raise ValueError("Ticker does not exist!")	
		stock = [x.text.strip() for x in data.findAll('span')]
		retrieved = datetime.datetime.now()-datetime.timedelta(minutes=15)
		cs = CompanyStock(stock[0], stock[1], stock[2], retrieved)
	return cs


def getIndustryStocks(tickers):
	"""
		Retrieves stock information from set of tickers (in a certain industry)
	"""
	stocks = {}
	for ticker in tickers:
		response = requests.get('http://m.londonstockexchange.com/exchange/mobile/stocks/summary.html?tidm='+ticker)
		if (response.status_code == 200):
			soup = bs4.BeautifulSoup(response.content, "lxml")
			data = soup.find("div", {"class": "tr darkEven"})
			stock = [x.text.strip() for x in data.findAll('span')]
			retrieved = datetime.datetime.now()-datetime.timedelta(minutes=15)
			stocks[ticker] = CompanyStock(stock[0], stock[1], stock[2], retrieved)
	return stocks



def getHistoricalStockInformation(ticker, start, end):
	if datetime.datetime.now() < end:
		raise ValueError("This date range goes into the future!")
	if start < (datetime.datetime.now() - datetime.timedelta(days=366)):
		raise ValueError("Date range goes to far in the past!")
	return web.DataReader(ticker, "google", start, end)
		
