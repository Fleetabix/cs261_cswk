import feedparser
import requests
import bs4

class NewsInformation:
	def __init__(self, url, headline, image, article_date):
		self.url = url
		self.keywords = list()
		self.headline = headline
		self.image = image
		self.date_published = article_date


def getNews(ticker):
	news = list()
	webpage = 'https://finance.google.com/finance/company_news?q='+ticker+'&ei=OwiKWrHYB5CWUo31grgL&output=rss'
	f = feedparser.parse(webpage)
	for stories in f.entries:
		news.append(NewsInformation(stories.link, stories.title, getImage(url), ""))
	return news

def getImage(url):
	response = requests.get(url)
	image_url = ""
	if (response.status_code == 200):
		soup = bs4.BeautifulSoup(response.content, "lxml")
		image = soup.find("meta",  property="og:image")
		image_url = image["content"]	
	return image_url