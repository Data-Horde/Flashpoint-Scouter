import os,sys,json,re

# JSON Checks

def ReadConfig(jsonfile='config.json'):
	"""Read json config"""
	assert (os.path.exists(jsonfile)), "{} is missing.\nUntil we add something to generate a new config.json we are going to have to ask you to re-install.\nSorry :{".format(jsonfile)
	
	#Check to see if config is loadable
	#assert (type(JSON) == type(dict())), "config.json does not seem to be an object."

	JSON = {}
	try:
		with open(jsonfile,"r") as config:
			JSON = json.load(config)
	except:
		raise Exception("{} is not a valid json object".format(jsonfile))

	return JSON

def GetURLPrefix(CONFIG,fname='the configuration file'):
	"""Read URLPrefix in config"""
	assert ("URLPrefix" in CONFIG), "URLPrefix key is missing in {} !".format(fname)
	
	URLPrefix = CONFIG["URLPrefix"]

	#Check to see that it's valid
	assert (URLPrefix!=""), "Please specify the URLPrefix for your target in config.json"

	return URLPrefix

def GetURLSuffix(CONFIG,fname='the configuration file'):
	"""Read URLSuffix in config"""
	assert ("URLSuffix" in CONFIG), "URLSuffix key is missing in {} !".format(fname)
	
	URLSuffix = CONFIG["URLSuffix"]

	#URLSuffix CAN be empty
	#assert (URLSuffix!=""), "Please specify the URLSuffix for your target in config.json"

	return URLSuffix

