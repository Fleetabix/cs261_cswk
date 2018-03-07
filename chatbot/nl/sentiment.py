from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

def getSentiment(sentence):
    if sentence is None or sentence == "":
        return {"compound":0.0}
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(sentence)
    return ss
