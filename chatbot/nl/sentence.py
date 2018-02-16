import nltk
import dict
import string

class Sentence:
    __doc__="A class for natural language sentences"

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = nltk.word_tokenize(sentence)

    def extract(self):
        return self.findFromDictionary("qualities", self.tokens)

    def findFromDictionary(self, dictName, tokens):
        dictionary = dict.getDict(dictName)
        length = len(tokens) #Start with the full string.
        while length>0:
            for i in range(0,len(tokens)-length+1): #Every group of length length.
                name = tokensToSentence(tokens[i:i+length]) #Find the potential name
                actualName = getID(name, dictionary)
                if actualName != None: #If name is an alias:
                    newList = tokens[:i] + tokens [i+length:]
                    return [actualName] + self.findFromDictionary(dictName, newList) #Recursion
            length-=1 #Now check shorter strings.
        return []

def getID(name, dictionary):
    for entry in dictionary:
        for alias in entry["alias"]:
            if alias == name:
                return entry["id"]

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
