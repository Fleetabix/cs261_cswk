from chatbot.nl.sentence import Sentence
from chatbot.nl import dict

#Returns the requests found in an input string.
def getRequests(s):
	sentence = Sentence(s)
	sentence.extract()
	return sentence.queries

#Returns a message based to indicate that the query wasn't understood.
def genericUnknownResponse():
	message = "I'm sorry, I didn't understand that."
	return turnIntoResponse(message)

chatbotName = "FLORIN"

def turnIntoResponse(body):
	return {
			"type": "text",
			"body": body,
			"caption" : None
		}

def turnIntoResponseWithCaption(body, caption):
	return {
			"type": "text",
			"body": body,
			"caption" : caption
		}

def turnIntoBarChart(labels, datasets, body):
	return {
		"type": "chart",
		"chart_object": {
			"type": "bar",
			"data": {
				"labels": labels,
				"datasets": datasets
			}
		},
		"description": body
	}

def turnChartIntoChartResponse(chart, description):
	return	{
				"type":"chart",
				"chart_object":chart,
				"description":description
			}

def printDate(date):
	return date.strftime('%d/%m/%y')

def printCompanyList():
	print(dict.getDict("companies"))

def printAsSterling(amount):
	amount = '£{:,.2f}'.format(amount)
	return amount

def printAsPercent(amount):
	amount = str(amount) + "%"
	return amount

#Turn a set of objects into a comma and and seperated list.
def makeList(segments):
	counter = len(segments)
	sentence = ""
	for segment in segments:
		sentence+=segment
		counter -= 1
		if counter == 1:
			sentence+=" and "
		elif counter>1:
			sentence+=", "
	return sentence

#Turn a set of objects into a comma and or seperated list.
def makeOrList(segments):
	counter = len(segments)
	sentence = ""
	for segment in segments:
		sentence+=segment
		counter -= 1
		if counter == 1:
			sentence+=" or "
		elif counter>1:
			sentence+=", "
	return sentence

def turnIntoArticle(title, description, url, pic_url):
	return	{
			    "title": title,
				"description": description,
				"url": url,
				"pic_url": pic_url
			}

def turnIntoNews(articles):
    return  {
                "type": "news",
                "articles": articles
            }

#Make a term possessive (term's)
def posessive(term):
	if term.endswith("s"):
		return term+"'"
	return term+"'s"
