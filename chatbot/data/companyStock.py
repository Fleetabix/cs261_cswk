class CompanyStock:
	def __init__(self, spotprice, change, percentchange):
		self.spot_price = spotprice
		self.price_difference = change
		self.percent_difference = percentchange
		self.retrieved = retrieve_datetime
