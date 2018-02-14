import os
import json

def read(dictName):
    #Dictionaries are stored in a subdirectory, so modify the path.
    path = os.path.join("dictionaries",dictName)
    #Try to open the file.
    f = openFile(path)
    #Don't try to read a missing file.
    if f is None:
        return None
    #Read the file and convert it from JSON.
    data = f.read()
    return json.loads(data)

def openFile(fileName):
	path=os.path.dirname(__file__)
	path=os.path.join(path,fileName)
	try:
		return open(path)
	except IOError:
		return None
