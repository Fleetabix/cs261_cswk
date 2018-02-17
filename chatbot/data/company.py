from stockHandler import CompanyStock, StockHandler
class Company:

	def __init__(self, comp_name, ticker_name):
		self.fullname = comp_name
		self.ticker = ticker_name
	
	def getSpotPrice(self):
		return StockHandler.getStockInformation(self.ticker).spot_price

	def getSpotPriceDifference(self):
		return StockHandler.getStockInformation(self.ticker).price_difference

	def getSpotPercentageDifference(self):
		return StockHandler.getStockInformation(self.ticker).percent_difference)
