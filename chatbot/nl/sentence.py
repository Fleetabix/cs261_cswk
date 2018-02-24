import nltk
import dict, timePhrase
import string

class Sentence:
	__doc__="A class for natural language sentences"

	#Refers to the previous noun/nouns mentioned.
	it = {"dictionary":"connectives", "id":"it", "typed":None}

	def __init__(self, sentence):
		self.sentence = sentence
		self.tokens = tokenise(sentence)

	def extract(self):
		#Look for key phrases in the text.
		dictionaries = ["qualities", "comparatives", "connectives", "companies", "areas"]
		self.keywords = self.findFromDictionaries(dictionaries, self.tokens)
		#Remove the punctuation in order to check for time phrases.
		punctTranslator = str.maketrans('', '', string.punctuation)
		punctFree = self.sentence.translate(punctTranslator)
		self.time = timePhrase.getDate(punctFree, tokenise(punctFree))
		#Give a default.
		if self.time is None:
			self.time = timePhrase.current()
		#Make sure that time flows forward.
		else:
			self.time = timePhrase.fixDate(self.time)
		#Sort the keywords that have been found into something meaningful.
		self.removeIts()
		self.organiseKeywords()

	#Replace all instances of "it" or its alias with the previous company or area.
	def removeIts(self):
		newKeywords = []
		for word in self.keywords:
			if word["dictionary"] == "companies" or word["dictionary"] == "areas":
				Sentence.it = word
				newKeywords.append(word)
			elif word["id"] == "it":
				newKeywords.append(Sentence.it)
			else:
				newKeywords.append(word)
		self.keywords = newKeywords


	#Organise the keywords into a tree structure to show connections.
	def organiseKeywords(self):
		newKeywords = []
		#Search for missing "and" tokens in lists of similar keywords
		for index, word in enumerate(self.keywords):
			#Copy the word into the new list.
			newKeywords.append(word)
			#As long as this isn't the last element of the list...
			if index < (len(self.keywords) - 1):
				#Grab the next word.
				nextWord = self.keywords[index + 1]
				#Check which dictionaries the keywords are both from.
				dict1 = word["dictionary"]
				dict2 = nextWord["dictionary"]
				#If the dictionaries are of the right type and match...
				if (dict1 == "qualities" and dict2 == "qualities") or (dict1 == "companies" and dict2 == "companies"):
					#Add an extra "and" token between them.
					newKeywords.append({"dictionary":"connectives", "id":"and", "typed":None})
		self.keywords = newKeywords

		newKeywords = []
		#Distinguish between list and and seperator ands:
		#Additionally, get rid of "and" as the first or last keyword.
		for index, word in enumerate(self.keywords):
			#If this word is marked "and"
			if word["id"] == "and":
				#As long as this isn't the last element of the list...
				if index < (len(self.keywords) - 1):
					#Grab the next word.
					nextWord = self.keywords[index + 1]
					#Ignore duplicate "and"s.
					if nextWord["id"] != "and":
						#As long as this isn't the first element of the list...
						if index > 0:
							#Grab the previous word.
							prevWord = self.keywords[index - 1]
							#Check which dictionaries the keywords are both from.
							dict1 = prevWord["dictionary"]
							dict2 = nextWord["dictionary"]
							if (dict1 == "qualities" and dict2 == "companies") or (dict1 == "companies" and dict2 == "qualities"):
								newKeywords.append({"dictionary":"connectives", "id":"seperator", "typed":word["typed"]})
							else:
								#Copy the word into the new list.
								newKeywords.append(word)
			else:
				#Copy the word into the new list.
				newKeywords.append(word)
		self.keywords = newKeywords
		#The queries object holds each indiviual query
		queries = []
		query = {"companies":[],"qualities":[],"areas":[],"comparative":None}
		#Read the keywords up to a seperator character.
		for word in self.keywords:
			if word["id"] == "seperator":
				queries.append(query)
				query = {"companies":[],"qualities":[],"areas":[],"comparative":None}
			elif word["dictionary"] == "companies":
				query["companies"].append(word["id"])
			elif word["dictionary"] == "qualities":
				query["qualities"].append(word["id"])
			elif word["dictionary"] == "areas":
				query["areas"].append(word["id"])
			elif word["dictionary"] == "comparative" and query["comparative"] == None:
				query["comparative"] = word["id"]
		#Add the final query
		queries.append(query)
		#Now read through to seperate "qualities" into individual queries.
		self.queries = []
		for q in queries:
			for quality in q["qualities"]:
				newQuery = {"companies":q["companies"],"areas":q["areas"],"quality":quality,"comparative":q["comparative"],"time":self.time}
				self.queries.append(newQuery)

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

	#Gives a printable representation of the sentence object.
	def __repr__(self):
		listOfWords = ""
		for keyword in self.keywords:
			showName = getShowName(keyword["id"], keyword["dictionary"])
			if showName is None:
				listOfWords+="?"
			else:
				listOfWords+=showName
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

def getShowName(id, dictName):
	dictionary = dict.getDict(dictName)
	if dictionary is None:
		return None
	for entry in dictionary:
		if wordsMatch(entry["id"],id):
			return entry["showName"]

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
