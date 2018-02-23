import feedparser
import datetime
import pandas_datareader.data as web


class CompanyStock:
	def __init__(self, spotprice, change, percentchange, retrieve_datetime):
		self.spot_price = spotprice
		self.price_difference = change
		self.percent_difference = percentchange
		self.retrieved = retrieve_datetime

def getStockInformation(ticker): 
	# [possibly] Temporary rss feed for now - till better one is found - current implementation is slow
	f = feedparser.parse('https://arcane-citadel-48781.herokuapp.com/')
	for stockinfo in f.entries:
		current_item = stockinfo.summary.split(',')
		if (current_item[0] == ticker):
			return CompanyStock(current_item[4], current_item[5], current_item[6], f.feed.updated)

def getHistoricalStockInformation(ticker, start, end):
	data = web.DataReader(ticker, "google", start, end)
	return data
		
