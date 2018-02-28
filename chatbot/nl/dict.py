import os
import json
from chatbot.models import *

#A dictionary of saved dictionaries.
dicts = {}

def getDict(string):
    #Check whether the string is already loaded
    if string in dicts:
        return dicts[string]
    #If it's not found, try to read it.
    d = read(string+".json")
    dicts[string] = d
    return d

def read(dictName):
    if dictName == "companies.json":
        return readCompanies()
    elif dictName == "areas.json":
        return readIndustries()
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

def readCompanies():
    dictionary = []
    for company in Company.objects.all():
        records = Company.objects.get(id = company.id).companyalias_set.all()
        id = company.ticker
        showname = id
        aliases = []
        for alias in records:
            aliases.append(alias.alias)
        dictionary.append({"id":id, "showname":showname, "alias":aliases})
    return dictionary

def readIndustries():
    dictionary = []
    for industry in Industry.objects.all():
        records = Industry.objects.get(id = industry.id).industryalias_set.all()
        id = industry.name
        showname = id
        aliases = []
        for alias in records:
            aliases.append(alias.alias)
        dictionary.append({"id":id, "showname":showname, "alias":aliases})
    return dictionary

def openFile(fileName):
	path=os.path.dirname(__file__)
	path=os.path.join(path,fileName)
	try:
		return open(path)
	except IOError:
		return None
