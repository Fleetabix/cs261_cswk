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
	if (response.status_code ==  200)
		response = requests.get(url)
		json_data = json.loads(response.text)
		for stories in json_data["articles"]:
			news.append(NewsInformation(stories["url"], stories["title"], stories["urlToImage"], stories["publishedAt"]))
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