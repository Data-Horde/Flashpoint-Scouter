import pandas as pd
from tqdm import tqdm

class Comparer:
    """A class for comparing strings in different fields"""
    def __init__(self, masterData, grabData, name):
        "INIT"
        self.M = pd.read_csv(masterData)["Title"]
        self.G = pd.read_csv(grabData)["Title"]
        self.name = name

    def __compare__jaroWinkler(self):
        """Compute JaroWinkler Similarity"""
        pass

    def __compare__exact(self,a,b):
    	return a==b

    def Compare(self, limit=-1):
        """Compare strings in masterdata and grabdata"""

        L = len(self.G)

        matches = pd.DataFrame()
        matches["Title"] = self.G.copy()
        matches["Match"] = ["NO"]*L
        #print(matches)
        
        R = range(L) if (limit==-1) else range(min(limit,L))
        for i in tqdm ( R, desc="Comparing game titles"):
            needle = self.G.loc[i]
            for j in range(len(self.M)):
                haystack = self.M.loc[j]
                if self.__compare__exact(needle,haystack):
                    #print("perfect match!")
                    matches["Match"][i] = "YES"
                    break

        matches.to_csv( '{}-rundown.csv'.format(self.name) )

        mismatches=matches[matches["Match"]=="NO"]
        mismatches.to_csv( '{}-mismatches.csv'.format(self.name) )

        perfectmatches=matches[matches["Match"]=="YES"]
        perfectmatches[matches["Match"]=="YES"].to_csv( '{}-perfectmatches.csv'.format(self.name) )
        
        return matches