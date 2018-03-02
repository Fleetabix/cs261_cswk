import parsedatetime
from datetime import datetime
from chatbot.nl import sentence, dict

#Returns the dates retrieved from a string, or None if there is no date.
def getDate(s, tokens):
    now = datetime.now()
    #Create a calendar object.
    cal = parsedatetime.Calendar()
    #Parse the string, storing the date found in date.
    #success shows whether the parse found a date there.
    date, success = cal.parse(s)
    #A success value of zero, indicates that no date or time was found.
    if success == 0:
        return None
    #Grab the time-phrase dictionary
    dictionary = dict.getDict("time")
    #If it's not found, just use a blank list instead.
    if dictionary is None:
        dictionary = []
    #Check for a "since" token. If it's found, return from the date til now.
    for token in tokens:
        if sentence.getID(token, dictionary) == "since":
            d = datetime(*date[:6])
            return {"start":d,"end":now}
    #If there's not enough tokens to split into 2 dates, return what we have.
    if len(tokens) <=3:
        #Convert to a datetime object.
        d = datetime(*date[:6])
        #Only one date, so it's the start and the end.
        return {"start":d,"end":d}
    #Check for two dates in one phrase, with at least some dividing token.
    #We're going to check for two dates, seperated by one word that's not a date.

    #Start the first potential date short.
    string1Length = 1
    #We're only looking for one word in the middle.
    middleStringLength = 1
    #The second string starts off as all remaining words.
    string2Length = len(tokens) - middleStringLength - string1Length

    #Keep going whilst the length of the second string is positive.
    while string2Length>0:
        #Grab the first words of the tokens for the first string.
        tokens1 = tokens[:string1Length]
        #Turn it into a properly formatted sentence.
        string1 = sentence.tokensToSentence(tokens1)
        #Grab the last words of the tokens for the second string.
        tokens2 = tokens[-string2Length:]
        #Also turn it into a properly formatted sentence.
        string2 = sentence.tokensToSentence(tokens2)
        #The middle tokens are the ones between the end of 1st and start of 2nd.
        middleTokens = tokens[string1Length:-string2Length]
        #Turn these tokens into a formatted sentence too. (Just one word)
        middleString = sentence.tokensToSentence(middleTokens)
        #Try to discern a date from the first and second strings.
        date1 = getDate(string1, tokens1)
        date2 = getDate(string2, tokens2)
        #Check whether the middle string is a "joining word"
        middleJoiningWord = sentence.getID(middleString, dictionary) == "to"

        #What we're looking for is for both strings 1 and 2 to be dates,
        #but for the middle string to not count as a date.
        if(date1 is not None and date2 is not None and middleJoiningWord):
            return {"start":date1["start"],"end":date2["start"]}
        #If we don't meet the condition, continue by changing the string sizes.
        string1Length+=1
        string2Length-=1
    #If nothing else, return the date we did find

    #Convert to a datetime object.
    d = datetime(*date[:6])
    #Only one date, so it's the start and the end.
    return {"start":d,"end":d}

#Make sure that the start time is before the end time.
def fixDate(d):
    if d["start"]>d["end"]:
        temp = d["start"]
        d["start"] = d["end"]
        d["end"] = temp
    return d

#Get the current time
def current():
    now = datetime.now()
    return {"start":now,"end":now,"now":True}
