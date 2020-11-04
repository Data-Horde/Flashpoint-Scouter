import os,sys,json,re

# JSON Checks

def CheckConfigExists():
	#Check to see if config exists
	assert (os.path.exists('config.json')), "config.json is missing.\nUntil we add something to generate a new config.json we are going to have to ask you to re-install.\nSorry :{"
	#Check to see if config is loadable

	#assert (condition), "error"
	JSON = {}
	return JSON

def CheckURLPrefix(JSON):

	#Check to see that there is indeed a URLPrefix item in config.json

	#Check to see that its valid

    #assert (condition), "error"

    return URLPrefix