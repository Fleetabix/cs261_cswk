import nl
import timePhrase, nltk
import sys

while(1):
    i = input("TIME>")
    o = timePhrase.getDate(i, nltk.word_tokenize(i))
    if o is None:
        print("Nothing found.")
    else:
        print(o["start"])
        print(o["end"])
    #print(nl.getResponse(input(">")))
