import nltk

class Sentence:
    __doc__="A class for natural language sentences"

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = nltk.word_tokenize(sentence)

    def extract(self):
        return self.tokens
