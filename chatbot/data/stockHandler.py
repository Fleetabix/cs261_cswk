import feedparser

class CompanyStock:
	def __init__(self, spotprice, change, percentchange):
		self.spot_price = spotprice
		self.price_difference = change
		self.percent_difference = percentchange

class StockHandler:

	def getStockInformation(ticker): 
		# [possibly] Temporary rss feed for now - till better one is found - current implementation is slow
		feed = feedparser.parse('https://arcane-citadel-48781.herokuapp.com/')
		for i in range(1, len(feed)):
			current_item = feed.entries[i].summary.split(',')
			if (current_item[0] == ticker):
				return CompanyStock(current_item[4], current_item[5], current_item[6])
	
