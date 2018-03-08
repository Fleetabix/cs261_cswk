import requests
import bs4
import json
import datetime

class NewsInformation:
	def __init__(self, url, headline, image, description, article_date):
		self.url = url
		self.headline = headline
		self.image = image
		self.description = description
		self.date_published = datetime.datetime.strptime(article_date[:19], '%Y-%m-%dT%H:%M:%S')

	def get_str_date(self, format="%Y-%m-%d | %H:%M:%S"):
		return datetime.datetime.strftime(self.date_published, format)

	def toJson(self):
		return {
			"title": self.headline,
			"url": self.url,
			"pic_url": self.image,
			"description": self.description,
			"date": self.get_str_date()
		}

	
def getNews(name, keyword = None, breaking = None):
	"""
		Function to retrieve news, optional parameters allow for specific topics or
		breaking news to be added.
	"""
	news = list()
	search_query = ""
	if keyword is not None:
		search_query = name+" "+keyword
		search_query = search_query.replace('&', ' and ').replace('/',' or ').replace(' ', '%20')
	else:
		search_query = name.replace('&', ' and ').replace('/',' or ').replace(' ', '%20')

	if breaking:
		url =  'https://newsapi.org/v2/top-headlines?q='+search_query+'&language=en&apiKey=d9c204a671844e58b110128b0b806c1f'
	else:
		url = 'https://newsapi.org/v2/everything?q='+search_query+'&language=en&apiKey=d9c204a671844e58b110128b0b806c1f'

	response = requests.get(url)

	if (response.status_code ==  200):
		json_data = json.loads(response.text)
		for stories in json_data["articles"]:
			news.append(NewsInformation(stories["url"], stories["title"], stories["urlToImage"], stories["description"], stories["publishedAt"]))
	else:
		raise RuntimeError("Unable to retrieve response from NewsAPI.")
	return news

