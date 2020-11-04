#Startup Routines

#Imports
from core.checks import *

#Attempt Crawl
def AttemptCrawl():

	print('Working...')

	CONFIG = CheckConfigExists()
	#URL-PREFIX METHOD
	URLPrefix = CheckURLPrefix(CONFIG)
	print(URLPrefix)