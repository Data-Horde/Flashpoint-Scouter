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
        try:
            response = self.s.get(URL).status_code
        except requests.exceptions.ConnectionError as e:
            return None

    #ID-Based Crawl
    def CrawlById(self,prefix,suffix):
        last_status_code = 200
        #while last_status_code == 200:
        #Don't forget 0 index (IF it does exist)
        target = prefix+str(1)+suffix
        self.getStatusCode(target)

    #Attempt Crawl

    def AttemptCrawl(self, crawlMethod='id', urlFormat='pre+suf'):

        if crawlMethod == 'id' and urlFormat == 'pre+suf':

            URLPrefix = GetURLPrefix(self.CONFIG)
            URLSuffix = GetURLSuffix(self.CONFIG)

            print("Todo: implement save/loading counts and cookies from json!")

            #Determine Limit
            LIMIT = 0

            #Check 0 index

            #Check 1 index and try powers of two
            results = self.CrawlById(URLPrefix,URLSuffix)
            return results

        else:
        	print("Unknown crawlMethod or urlFormat when attempting crawl!")
        	return []

    ###########################
    #Doesn't take self
    ###########################


