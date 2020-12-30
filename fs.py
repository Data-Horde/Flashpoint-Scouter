# 3rd Party Imports
import requests

# Internal Imports
from core.crawler import *
from core.comparer import *

def main():
    # PHASE 0: Initialization
    #New Session, you might want to reuse this later on
    s = requests.Session()
    
    CRWLER = Crawler(s)
    # TODO: CHANGE THIS SO CONFIG IS LOADED AND THEN PASSED TO CRWLER!
    CRWLER.loadConfig()

    # PHASE 1: Initial Crawl
    CRWLER.AttemptCrawl()
    #print(CRWLER.links)

    # PHASE 2: GRAB 
    # TODO: (MAKE A NEW CLASS FOR THIS)
    grabfile = CRWLER.Grab()

    # PHASE 3: COMPARE
    CMPRER = Comparer("GML.csv",grabfile,CRWLER.CONFIG.name)
    matches = CMPRER.Compare()

    print(matches)

    matchpercent = (len(matches[matches["Match"]=="YES"])/len(matches) * 100)
    print("Match percentage: {}%".format(matchpercent))

if __name__ == "__main__":
    main()