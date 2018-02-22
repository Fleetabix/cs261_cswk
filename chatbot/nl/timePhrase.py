import parsedatetime
from datetime import datetime
import sentence
import dict

#Returns the dates retrieved from a string, or None if there is no date.
def getDate(s, tokens):
    #Create a calendar object.
    cal = parsedatetime.Calendar()
    #Parse the string, storing the date found in date.
    #success shows whether the parse found a date there.
    date, success = cal.parse(s)
    #A success value of zero, indicates that no date or time was found.
    if success == 0:
        return None
    #Grab the time-phrase dictionary
    dictionary = dict.getDict("time.json")
    #If it's not found, just use a blank list instead.
    if dictionary is None:
        dictionary = []
    #Check for a "since" token. If it's found, return from the date til now.
    for token in tokens:
        if sentence.getID(token, dictionary) == "since":
            d = datetime(*date[:6])
            now = datetime.now()
            return {"start":d,"end":now}
    #If there's not enough tokens to split into 2 dates, return what we have.
    if len(tokens) <=3:
        #Convert to a datetime object.
        d = datetime(*date[:6])
        #Only one date, so it's the start and the end.
        return {"start":d,"end":d}
    #Check for two dates in one phrase, with at least some dividing token.
    string1Length = 1
    middleStringLength = 1
    string2Length = len(tokens) - middleStringLength - string1Length
    print(str(string1Length) + str(middleStringLength) + str(string2Length))
    while string2Length>0:
        tokens1 = tokens[:string1Length]
        string1 = sentence.tokensToSentence(tokens1)
        tokens2 = tokens[(0-string2Length):]
        string2 = sentence.tokensToSentence(tokens2)
        middleTokens = tokens[string1Length:(0-string2Length)]
        middleString = sentence.tokensToSentence(middleTokens)
        date1 = getDate(string1, tokens1)
        date2 = getDate(string2, tokens2)
        middleDate = getDate(middleString, middleTokens)
        print(string1 + "|" + middleString + "|" + string2)
        print(tokens1 + middleTokens + tokens2)
        print(str(string1Length) + str(middleStringLength) + str(string2Length))
        if(date1 is not None and date2 is not None and middleTokens is None):
            return {"start":date1["start"],"end":date2["start"]}
        string1Length+=1
        string2Length-=1
    #If nothing else, return the date we did find

    #Convert to a datetime object.
    d = datetime(*date[:6])
    #Only one date, so it's the start and the end.
    return {"start":d,"end":d}
