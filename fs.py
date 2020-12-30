# 3rd Party Imports
import requests

# Internal Imports
from core.crawler import *

def main():
    
    # PHASE 0: Initialization
    #New Session, you might want to reuse this later on
    s = requests.Session()
    
    CRWLER = Crawler(s)
    CRWLER.loadConfig()

    # PHASE 1: Initial Crawl
    CRWLER.AttemptCrawl()
    #print(CRWLER.links)

    # PHASE 2: TITLE/GAMEFILE SELECTION
    CRWLER.SelectTitle()
    #CRWLER.SelectGame()

    # PHASE 3: GRAB
    CRWLER.Grab(limit=10)

    # PHASE 4: COMPARE

if __name__ == "__main__":
    main()