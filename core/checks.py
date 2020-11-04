import os,sys,json,re

# JSON Checks

def CheckConfigExists():
	#Check to see if config exists
	assert (os.path.exists('config.json')), "config.json is missing.\nUntil we add something to generate a new config.json we are going to have to ask you to re-install.\nSorry :{"
	
	#Check to see if config is loadable
	#assert (type(JSON) == type(dict())), "config.json does not seem to be an object."

	JSON = {}
	try:
		with open('config.json',"r") as config:
			JSON = json.load(config)
	except:
		raise Exception("config.json is not a valid json object")

	return JSON

def CheckURLPrefix(CONFIG):
	#Check to see that there is indeed a URLPrefix item in config.json
	assert ("URLPrefix" in CONFIG), "config.json URLPrefix key is missing"
	
	URLPrefix = CONFIG["URLPrefix"]

	#Check to see that it's valid
	assert (URLPrefix!=""), "Please specify the URLPrefix for your target in config.json"

	return URLPrefix