import feedparser
import requests
import bs4
import json
import time

class NewsInformation:
	def __init__(self, url, headline, image, article_date):
		self.url = url
		self.headline = headline
		self.image = image
		self.date_published = article_date

def benchmark():
	start = time.time()
	getNews('WTB')
	end = time.time()
	print(end-start)
	start = time.time()	
	getNewsNewsAPI('whitbread')
	end = time.time()
	print(end-start)
	

def getNewsNewsAPI(company_name, keyword = None):
	news = list()
	if keyword is None:
		company_name = company_name.replace(' ', '%20')
		url = 'https://newsapi.org/v2/everything?q='+company_name+'&apiKey=d9c204a671844e58b110128b0b806c1f'
		response = requests.get(url)
		json_data = json.loads(response.text)
		for stories in json_data["articles"]:
			news.append(NewsInformation(stories["url"], stories["title"], stories["urlToImage"], stories["publishedAt"]))
	

def getNews(ticker):
	news = list()
	webpage = 'https://finance.google.com/finance/company_news?q='+ticker+'&ei=OwiKWrHYB5CWUo31grgL&output=rss'
	f = feedparser.parse(webpage)
	for stories in f.entries:
		image_url = getImage(stories.link)
		date_published = stories.published
		news.append(NewsInformation(stories.link, stories.title, image_url, date_published))
	return news


def getImage(url):
	response = requests.get(url)
	image_url = ""
	if (response.status_code == 200):
		soup = bs4.BeautifulSoup(response.content, "lxml")
		image = soup.find("meta",  property="og:image")
		if image is not None:
			image_url = image["content"]	
	return image_url