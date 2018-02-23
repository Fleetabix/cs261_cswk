import nltk
import dict, timePhrase
import string

class Sentence:
	__doc__="A class for natural language sentences"

	def __init__(self, sentence):
		self.sentence = sentence
		self.tokens = tokenise(sentence)

	def extract(self):
		#Look for key phrases in the text.
		dictionaries = ["qualities", "comparatives", "connectives", "companies"]
		self.keywords = self.findFromDictionaries(dictionaries, self.tokens)
		#Remove the punctuation in order to check for time phrases.
		punctTranslator = str.maketrans('', '', string.punctuation)
		punctFree = self.sentence.translate(punctTranslator)
		self.time = timePhrase.getDate(punctFree, nltk.word_tokenize(punctFree))
		#Give a default.
		if self.time is None:
			self.time = timePhrase.current()
		#Make sure that time flows forward.
		else:
			self.time = timePhrase.fixDate(self.time)
		#Sort the keywords that have been found into something meaningful.
		self.organiseKeywords()

	def organiseKeywords(self):
		pass

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
		output = listOfWords
		if self.time is not None:
			output += "\n" + str(self.time["start"])
			output += " - " + str(self.time["end"])
		return output

def tokenise(sentence):
	tokens = nltk.word_tokenize(sentence)
	tagged = nltk.pos_tag(tokens)
	#Remove 's when it's a verb (Only need it as a possessive)
	untagged = []
	for tag in tagged:
		if tag[0] != "'s" or tag[1] != "VBZ":
			untagged.append(tag[0])
	return untagged

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
