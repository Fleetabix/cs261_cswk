from sentence import Sentence

#Returns the response to a given input string.
def getResponse(s):
	sentence = Sentence(s)
	sentence.extract()
	return sentence
