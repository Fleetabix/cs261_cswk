import os

def read(dictName):
	pass

def openFile(fileName):
	path=os.path.dirname(__file__)
	path=os.path.join(path,dictName)
	try:
		return open(path)
	except IOError:
		return None
