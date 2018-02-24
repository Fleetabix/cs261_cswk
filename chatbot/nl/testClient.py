import nl
import timePhrase, nltk
import sys

timeMode = False

while(1):
    if timeMode:
        i = input("TIME>")
        o = timePhrase.getDate(i, nltk.word_tokenize(i))
        if o is None:
            print("Nothing found.")
        else:
            print(o["start"])
            print(o["end"])
    else:
        print(nl.getResponse(input(">")))
