import nltk
import dict
import string

class Sentence:
	__doc__="A class for natural language sentences"

	def __init__(self, sentence):
		self.sentence = sentence
		self.tokens = nltk.word_tokenize(sentence)

	def extract(self):
		self.keywords = self.findFromDictionaries(["qualities", "comparatives", "connectives", "companies"], self.tokens)

	def findFromDictionaries(self, dictNames, tokens):
		#Make an empty list of dictionaries
		dictionaries = {}
		#Grab the corresponding dictionary and add it to the list.
		for dictName in dictNames:
			dictionary = dict.getDict(dictName)
			if dictionary is not None:
				dictionaries[dictName] = dictionary
		#Start with the full string:
		length = len(tokens)
		while length>0:
			for i in range(0,len(tokens)-length+1): #Every group of length length.
				name = tokensToSentence(tokens[i:i+length]) #Find the potential name
				actualName = getIDAndDictionary(name, dictionaries)
				if actualName != None: #If name is an alias:
					#Perform this on the words before the found word
					firstHalf = self.findFromDictionaries(dictNames, tokens[:i])
					#And on the words after the found word
					secondHalf = self.findFromDictionaries(dictNames, tokens[i+length:])
					#Combine them in the correct order.
					return firstHalf + [{"dictionary":actualName["dictionary"],"id":actualName["id"], "typed":name}] + secondHalf #Recursion
			length-=1 #Now check shorter strings.
		return []

	def __repr__(self):
		listOfWords = ""
		for keyword in self.keywords:
			listOfWords+=keyword["id"]
			listOfWords+=" "
		#return "Keywords: " + self.keywords.__repr__() + "\n" + listOfWords
		return listOfWords

def getID(name, dictionary):
	for entry in dictionary:
		for alias in entry["alias"]:
			if wordsMatch(alias,name):
				return entry["id"]

def getIDAndDictionary(name, dictionaries):
	for key in dictionaries:
		dictionary = dictionaries[key]
		for entry in dictionary:
			for alias in entry["alias"]:
				if wordsMatch(alias,name):
					return {"dictionary":key, "id":entry["id"]}

def wordsMatch(word1, word2):
	return word1.lower() == word2.lower()

#Takes a set of tokens and reassmbles them to make a normal sentence.
def tokensToSentence(tokens):
	spaceChar = "" #Skip the first space character.
	sentence = "" #Empty sentence to fill.
	for word in tokens:
		#Find out if it's punctuation, or an apostrophe-based token.
		if word in string.punctuation or "'" in word:
			sentence += word #Add to sentence without any space.
		else:
			sentence += spaceChar + word #Add with a space character.
		spaceChar = " " #After the first word, we want spaces again.
	return sentence
