#Startup Routines

#Imports
from core.checks import *

#Attempt Crawl
def AttemptCrawl():

	print('Working...')

	CONFIG = CheckConfigExists()

	#URL-PREFIX METHOD
	URLPrefix = CheckURLPrefix(CONFIG)
	URLSuffix = CheckURLSuffix(CONFIG)
	
	#Try powers of two
	#Don't forget 0 index
