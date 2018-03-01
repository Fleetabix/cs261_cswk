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
	

def getNews(name, keyword = None, breaking = None):
	"""
	    can be used for both industry and company
	"""
	news = list()
	search_query = ""
	if keyword is not None:
		search_query = name+" "+keyword
		search_query = search_query.replace('&', ' and ').replace('/',' or ').replace(' ', '%20')
	else:
		search_query = name.replace(' ', '%20')
	
	if breaking:
		url =  'https://newsapi.org/v2/top-headlines?q='+search_query+'&language=en&apiKey=d9c204a671844e58b110128b0b806c1f'
	else:
		url = 'https://newsapi.org/v2/everything?q='+search_query+'&language=en&apiKey=d9c204a671844e58b110128b0b806c1f'
    
	response = requests.get(url)

	if (response.status_code ==  200):
		json_data = json.loads(response.text)
		for stories in json_data["articles"]:
			news.append(NewsInformation(stories["url"], stories["title"], stories["urlToImage"], stories["publishedAt"]))
	return news

