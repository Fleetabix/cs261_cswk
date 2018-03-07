import feedparser
import datetime
import pandas_datareader.data as web
import requests
import datetime
import bs4

class CompanyStock:
	def __init__(self, spotprice, change, percentchange, volume, retrieve_datetime):
		self.spot_price = spotprice
		self.price_difference = change
		self.percent_difference = percentchange
		self.volume = volume
		self.retrieved = retrieve_datetime

def getStockInformation(ticker): 
	"""
		Retrieves stock information from a ticker for a specific company.
		Returns a CompanyStock object with specified information.
	"""

	# Retrive response from source for website
	if (ticker == 'UKX'):
		# Response from UKX (FTSE 100)
		response = requests.get('http://m.londonstockexchange.com/exchange/mobile/indices/summary.html?index=UKX')
	else:
		# Response from tickers within FTSE 100
		response = requests.get('http://m.londonstockexchange.com/exchange/mobile/stocks/summary.html?tidm='+ticker)
	cs = None
	if (response.status_code == 200):
		# Format webpage to retrieve particular stock information
		soup = bs4.BeautifulSoup(response.content, "lxml")
		data = soup.find_all("div", {"class": "tr darkEven"})

		# Catches cases where the website redirects to homepage due to nonexistent company
		if data is None:
			raise ValueError("Ticker does not exist!")

		stock = [x.text.strip() for x in data[0].findAll('span')]
		stock.append(data[1].find('span').text.strip())
		
		retrieved = datetime.datetime.now()
		# when markets are shut volume is nothing
		cs = CompanyStock(stock[0], stock[1], stock[2], '0' if stock[3] == '' else stock[3], retrieved)
	else:
		raise RuntimeError("Unable to retrieve response from London Stock Exchange website.")
	return cs


def getHistoricalStockInformation(ticker, start, end):
	"""
		Retrieves historical stocks of a company(s) within a year from specified ticker(s).
		Returns a pandas DataFrame with High, Low, Open and Close spot prices for each day
		between start and end dates.
	"""
	if not isinstance(start, datetime.datetime):
		start = datetime.datetime.combine(start, datetime.time.min)
	if not isinstance(end, datetime.datetime):
		end = datetime.datetime.combine(end, datetime.time.min)
	# Check whether dates are valid
	if datetime.datetime.now() < end:
		raise ValueError("This date range goes into the future!")
	if start < (datetime.datetime.now() - datetime.timedelta(days=366)):
		raise ValueError("Date range goes to far in the past!")

	# Use pandas_datareader to retrieve data remotely
	return web.DataReader(ticker, "google", start, end)
		
