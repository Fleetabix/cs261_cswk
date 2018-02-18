import feedparser

class NewsInformation:
	def __init__(self, url):
		self.url = url
		self.keywords = []
		self.headline = ''

class NewsHandler:
	def getNews(ticker):
		f = feedparser.parse('')