from stock_handler import CompanyStock
import stock_handler
import news_handler
class Company:
	def __init__(self, comp_name, ticker_name):
		self.fullname = comp_name
		self.ticker = ticker_name
	
	def getSpotPrice(self):
		return stock_handler.getStockInformation(self.ticker).spot_price

	def getSpotPriceDifference(self):
		return stock_handler.getStockInformation(self.ticker).price_difference

	def getSpotPercentageDifference(self):
		return stock_handler.getStockInformation(self.ticker).percent_difference

	def getStockHistory(self, start, end):
		return stock_handler.getHistoricalStockInformation(self.ticker, start, end)

	def getNews(self):		
		return news_handler.getNews(self.ticker)
