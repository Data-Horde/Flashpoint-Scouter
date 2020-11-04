#Startup Routines

#Imports
from core.checks import *

#Attempt Crawl
def AttemptCrawl():
	print('Working...')
	CONFIG = CheckConfigExists()
	#print(CONFIG)