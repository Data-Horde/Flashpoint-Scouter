#3rd Party Imports
import requests

#Internal Imports
from core.jsonutils import *

class Crawler:
    """A crawler class"""
    def __init__(self, session):
        self.s = session

        self.cnfname = ""
        self.CONFIG = {}

    ###########################
    #Takes self
    ###########################

    def loadConfig(self, jsonfile='config.json'):
        """
        Load a configuration file. "config.json" by default.
        """
        self.cnfname = jsonfile
        self.CONFIG = ReadConfig(jsonfile)

    def getStatusCode(self,URL):
        """
        Attempt to get a URL and return status code.
        Returns None if ConnectionError
        """
        return self.s.get(URL).status_code

    #ID-Based Crawl
    def CrawlById(self,prefix,suffix):

        

        #Determine Limit
        LIMIT = 0

        #Step 0
        #Check 0 index
        #IGNORE WHEN COUNTING, SINCE 0 GETS ITS OWN CHECK

        #Step 1: Find the Upper Bound
        #Check index 1 and try powers of two
        UB = 1
        #Introduce skips ot avoid gaps!
        skips = 3
        used = 0

        last_status_code = 200
        while last_status_code == 200 or used < skips:

            target = self.idURL(prefix,UB+used,suffix)
            try:
                last_status_code = self.getStatusCode(target)
            except requests.exceptions.ConnectionError as e:
                print("Lost internet connection, retrying")
                continue
            
            #print(target)
            #print(UB+used, last_status_code)
            print(last_status_code, target)
    
            if last_status_code != 200:
                used+=1
            else:
                UB*=2
                used=0

        print("No more than {} items!".format(str(UB)))

        #Step 2: Binary Search the limit!

    #Attempt Crawl
    def AttemptCrawl(self, crawlMethod='id', urlFormat='pre+suf'):

        if crawlMethod == 'id' and urlFormat == 'pre+suf':

            URLPrefix = GetURLPrefix(self.CONFIG)
            URLSuffix = GetURLSuffix(self.CONFIG)

            print("Todo: implement save/loading counts and cookies from json!")

            results = self.CrawlById(URLPrefix,URLSuffix)
            return results

        else:
        	print("Unknown crawlMethod or urlFormat when attempting crawl!")
        	return []

    ###########################
    #Doesn't NEED self
    ###########################

    def idURL(self,prefix,id,suffix=''):
        return prefix+str(id)+suffix


