#Built-Ins
import os, sys

#3rd Party Imports
import requests
from selectolax.parser import HTMLParser
import pandas as pd
import time
from tqdm import tqdm

#Internal Imports
from core.config import *

class Crawler:
    """A crawler class"""
    def __init__(self, session):
        self.s = session
        self.CONFIG = Configuration()
        self.links = []

    ###########################
    #Instance Methods
    ###########################

    def loadConfig(self, file='config.json'):
        """
        Load a configuration file. "config.json" by default.
        """
        self.CONFIG.ReadConfig(file)

    def getStatusCode(self,URL):
        """
        Attempt to get a URL and return status code.
        Returns None if ConnectionError
        """
        return self.s.get(URL).status_code

    def getContents(self,URL):
        """
        Attempt to get a URL.
        Return status code and content
        Returns None if ConnectionError
        """
        request = self.s.get(URL)
        return request.status_code,request.content
    
    def getIdLimit(self, prefix, suffix):
        """
        Count upto the last id for a given website. 
        DocString goes here, follow the steps 0 through 3 for now.
        """

        #Step 0
        #Check 0 index
        #IGNORE WHEN COUNTING, SINCE 0 GETS ITS OWN CHECK
        print("Counting items by id...")

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
            #print(last_status_code, target)
    
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
        PARTITIONS = 10 #30
        #TRIES = 25
        used = 0 
        
        LB = UB//2
        UB -= 1

        #while UB - LB > THRESHOLD and used < TRIES:
        while UB - LB > THRESHOLD and used < PARTITIONS:
            DIFF = UB - LB

            #Random BAD
            #choice = random.choice([ (LB + x*DIFF//PARTITIONS) for x in range(1,PARTITIONS+1)])
            choice = (LB + (PARTITIONS-used-1)*DIFF//PARTITIONS)

            target = self.idURL(prefix,choice,suffix)
            try:
                last_status_code = self.getStatusCode(target)
            except requests.exceptions.ConnectionError as e:
                print("Unable to connect, retrying")
                continue
            #print("Stuck in a loop?")

            #print(last_status_code, target)
            #print(LB, choice, PARTITIONS-used-1)

            if last_status_code == 404:
                used+=1
            elif last_status_code == 200:
                #print("updating lower bound")
                LB=(LB + (PARTITIONS-used)*DIFF//PARTITIONS)
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

        print("COUNTING DOWN... This might take a minute...")
        #Step 3: Lower UB until we reach LB
        while UB > LB:
            target = self.idURL(prefix,choice,suffix)
            try:
                last_status_code = self.getStatusCode(target)
            except requests.exceptions.ConnectionError as e:
                print("Unable to connect, retrying")
                continue
            #print("Stuck in a loop?")

            #print(LB, UB)
            #print(last_status_code, target)

            if last_status_code == 404:
                UB-=1
            elif last_status_code == 200:
                #Update LB
                break

        return UB
    
    #ID-Based Crawl
    def CrawlById(self,prefix,suffix):

        #Determine Limit
        LIMIT = self.CONFIG.GetidCount()

        if not LIMIT:
        	LIMIT = self.getIdLimit(prefix,suffix)
        	print("Updating {}".format(self.CONFIG.filename))
        	self.CONFIG.dict["SiteInfo"] = {"idCount":LIMIT, "TitleSelector":""}
        	self.CONFIG.SaveConfig()

        return [ self.idURL(prefix,x,suffix) for x in range(LIMIT)]

    #Attempt Crawl
    def AttemptCrawl(self, crawlMethod='id', urlFormat='pre+suf'):

        if crawlMethod == 'id' and urlFormat == 'pre+suf':

            URLPrefix = self.CONFIG.GetURLPrefix()
            URLSuffix = self.CONFIG.GetURLSuffix()

            results = self.CrawlById(URLPrefix,URLSuffix)
            self.links += results

        else:
        	print("Unknown crawlMethod or urlFormat when attempting crawl!")
        	self.links += []


    def TrimHead(self):
        """
        Discard early links which are inaccesible
        """
        last_status_code = -1
        while last_status_code != 200:
            target = self.links[0]
            try:
                last_status_code = self.getStatusCode(target)
            except requests.exceptions.ConnectionError as e:
                print("Unable to connect, retrying")
                continue
            if last_status_code == 404:
                self.links = self.links[1:]
        #print(self.links[0])

    def SelectTitle(self):
    	"""
    	Ask for CSS title selector
    	"""
    	titleSelect = self.CONFIG.GetTitleCSS()
    	if titleSelect == "":
    		print("Title Selector unspecified, please add a css selector for the game titles under SiteInfo > TitleSelector in the configuration file: {}".format(self.CONFIG.filename))
    		quit()

    	#print("TODO: PREVIEW THIS SELECTOR")
    	pageContents,last_status_code="",-1
    	while last_status_code != 200:
    		target = self.links[0]
    		try:
    			last_status_code, pageContents = self.getContents(target)
    		except requests.exceptions.ConnectionError as e:
    			print("Unable to connect, retrying")
    			continue
    	titletree = HTMLParser(pageContents)
    	titlepreview = titletree.css_first(titleSelect).text()
    	print("Title Preview:")
    	print(titlepreview)

    	confirm = ""
    	while confirm!="y" and confirm!="n":
    		print("Does this game's title match? {} (y)es/(n)o".format(self.links[0]))
    		confirm=input()
    		if confirm=="n":
    			print("Please reconfigugre your the css selector for the game titles under SiteInfo > TitleSelector in the configuration file: {}".format(self.CONFIG.filename))
    			quit()


    def listFile(self):
        return self.CONFIG.name+"-list.csv"

    def checkGrabMade(self):
    	return os.path.exists(self.listFile())

    def Grab(self,sleep=0.0,limit=-1):
        """
        Begin grabbing games/game names!
        """

        #Abort if a grab was made
        if self.checkGrabMade():
        	return self.listFile()

        # TRIM HEAD
        self.TrimHead()
        # Select Title Check
        self.SelectTitle()
        # TODO: ADD GAME GRABBER HERE!

        last_status_code = -1
        gURLs,titles = [],[]
        progress=0
        L = len(self.links)
        R = range(L) if (limit==-1) else range(min(limit,L))
        for i in tqdm ( R, desc="Grabbing game titles"):
            if(sleep > 0.0):
                time.sleep(sleep)
            target = self.links[0]
            try:
                last_status_code, pageContents = self.getContents(target)
            except requests.exceptions.ConnectionError as e:
                print("Unable to connect, retrying")
                continue
            if last_status_code < 400 or last_status_code > 499:
                try:
                    titles.append(HTMLParser(pageContents).css_first(titleSelect).text())
                    gURLs.append(target)
                except:
                    print("Error: Skipping {}".format(target))
            self.links = self.links[1:]
        siteData = pd.DataFrame({"Title":titles,"URL":gURLs})
        siteData.to_csv('{}'.format(self.listFile()))
        return self.listFile()

    ###########################
    #Static Methods
    ###########################
    @staticmethod
    def idURL(prefix,id,suffix=''):
        return prefix+str(id)+suffix



