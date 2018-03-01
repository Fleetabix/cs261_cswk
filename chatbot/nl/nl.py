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

def printCompanyList():
	print(dict.getDict("companies"))
