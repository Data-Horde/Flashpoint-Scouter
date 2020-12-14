# 3rd Party Imports
import requests

# Internal Imports
from core.crawler import *

def main():
#New Session, you might want to reuse this later on
    s = requests.Session()
    
    CRWLER = Crawler(s)
    CRWLER.loadConfig()
    CRWLER.AttemptCrawl()

if __name__ == "__main__":
    main()