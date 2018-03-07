from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

def getSentiment(sentence):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(sentence)
    return ss
