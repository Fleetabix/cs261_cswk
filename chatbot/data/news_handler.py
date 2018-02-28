import feedparser
import requests
import bs4
import json
import time
import datetime

class NewsInformation:
	def __init__(self, url, headline, image, article_date):
		self.url = url
		self.headline = headline
		self.image = image
		self.date_published = datetime.datetime.strptime(article_date, '%Y-%m-%dT%H:%M:%SZ')

# def benchmark():
# 	start = time.time()
# 	print('using get news function')
# 	getNews('WTB')
# 	end = time.time()
# 	print(end-start)
# 	start = time.time()	
# 	print('using new get news function')
# 	getNewsNewsAPI('whitbread')
# 	end = time.time()
# 	print(end-start)
	
# need to mention powered by NewsAPI

"""
can be used for both industry and company
"""
def getNews(name, keyword = None):
	news = list()
	search_query = ""
	if keyword is not None:
		search_query = name+" "+keyword
		search_query = search_query.replace('&', ' and ').replace('/',' or ').replace(' ', '%20')
	else:
		search_query = name.replace(' ', '%20')
	url = 'https://newsapi.org/v2/everything?q='+search_query+'&apiKey=d9c204a671844e58b110128b0b806c1f'
	response = requests.get(url)
	json_data = json.loads(response.text)
	for stories in json_data["articles"]:
		news.append(NewsInformation(stories["url"], stories["title"], stories["urlToImage"], stories["publishedAt"]))
	return news
	

# def getNews(ticker):
# 	news = list()
# 	webpage = 'https://finance.google.com/finance/company_news?q='+ticker+'&ei=OwiKWrHYB5CWUo31grgL&output=rss'
# 	f = feedparser.parse(webpage)
# 	for stories in f.entries:
# 		image_url = getImage(stories.link)
# 		date_published = stories.published
# 		news.append(NewsInformation(stories.link, stories.title, image_url, date_published))
# 	return news


def getImage(url):
	response = requests.get(url)
	image_url = ""
	if (response.status_code == 200):
		soup = bs4.BeautifulSoup(response.content, "lxml")
		image = soup.find("meta",  property="og:image")
		if image is not None:
			image_url = image["content"]	
	return image_url