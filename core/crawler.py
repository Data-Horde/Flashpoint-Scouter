#Built-Ins
import random

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
    #Instance Methods
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
        """
        DocString goes here, follow the steps 0 through 3 for now.
        """

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
                print("Unable to connect, retrying")
                continue
            
            #print(target)
            #print(UB+used, last_status_code)
            print(last_status_code, target)
    
            if last_status_code == 404:
                used+=1
            elif last_status_code == 200:
                UB*=2
                used=0
            else:
                print('got status {}, retrying...'.format(last_status_code))
                continue

        print("No more than {} items!".format(str(UB)))
        used=0

        #Step 2: Find a reasonable lower bound

        #Key Assumption: Lower Bound is GUARANTEED to be accesible
        #Upper bound is GUARANTEED to have nothing beyond that point
        #Use a random number between lower bound and upper bound to determine the next lower bound

        THRESHOLD = 20
        PARTITIONS = 30
        TRIES = 25
        used = 0 
        
        LB = UB//2
        UB -= 1

        while UB - LB > THRESHOLD and used < TRIES:
            DIFF = UB - LB
            choice = random.choice([ (LB + x*DIFF//PARTITIONS) for x in range(1,PARTITIONS+1)])

            target = self.idURL(prefix,choice,suffix)
            try:
                last_status_code = self.getStatusCode(target)
            except requests.exceptions.ConnectionError as e:
                print("Unable to connect, retrying")
                continue
            #print("Stuck in a loop?")
            print(last_status_code, target)

            if last_status_code == 404:
                used+=1
            elif last_status_code == 200:
            	#Update LB
                LB=choice
                used=0
            else:
                print('got status {}, retrying...'.format(last_status_code))
                continue

        #If we run out of tries, lower the upper bound
        if UB - LB > THRESHOLD:
        	DIFF = UB - LB
        	UB = LB + DIFF//PARTITIONS

        #print(LB, UB)
        #print("LIMIT: {}".format(UB))

        #Step 3: Lower UB until we reach LB
        while UB > LB:
            target = self.idURL(prefix,choice,suffix)
            try:
                last_status_code = self.getStatusCode(target)
            except requests.exceptions.ConnectionError as e:
                print("Unable to connect, retrying")
                continue
            print("Stuck in a loop?")
            print(LB, UB)
            print(last_status_code, target)
            if last_status_code == 404:
                UB-=1
            elif last_status_code == 200:
            	#Update LB
                break

        LIMIT = UB
        print(LIMIT)

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
    #Static Methods
    ###########################
    @staticmethod
    def idURL(prefix,id,suffix=''):
        return prefix+str(id)+suffix


