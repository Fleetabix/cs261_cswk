import feedparser

class NewsInformation:
	def __init__(self, url, headline):
		self.url = url
		self.keywords = []
		self.headline = headline

class NewsHandler:
	def getNews(ticker):
		news = []
		f = feedparser.parse('https://finance.google.com/finance/company_news?q='+ticker+'&ei=OwiKWrHYB5CWUo31grgL&output=rss')
		for news in f.entries:
			news.append(NewsInformation(news.link, news.title))
		return news