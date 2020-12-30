import pandas as pd

class Comparer:
    """A class for comparing strings in different fields"""
    def __init__(self, masterData, grabData):
        "INIT"
        self.M = pd.read_csv(masterData)
        self.G = pd.read_csv(grabData)