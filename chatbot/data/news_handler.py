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
		for stories in f.entries:
			news.append(NewsInformation(stories.link, stories.title))
		return news