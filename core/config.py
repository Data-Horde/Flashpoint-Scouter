import os,sys,json,re

class Configuration:
    """A JSON Configuration Class"""
    def __init__(self, filename="newconfig.json", contents={}):
        self.filename = filename
        self.dict = contents

    def ReadConfig(self, jsonfile="config.json"):
        """Read json config"""
        assert (os.path.exists(jsonfile)), "{} is missing.\nUntil we add something to generate a new config.json we are going to have to ask you to re-install.\nSorry :{".format(jsonfile)
        
        #Check to see if config is loadable
        #assert (type(JSON) == type(dict())), "config.json does not seem to be an object."        
        JSON = {}
        try:
            with open(jsonfile,"r") as config:
                JSON = json.load(config)
        except:
            raise Exception("{} is not a valid json object".format(jsonfile))     
        #Read contents and rename placeholder filename to be used for writes
        self.dict = JSON
        self.filename = jsonfile

    def SaveConfig(self):
        """Save Config to file"""
        with open(self.filename,"w") as config:
            JSON = json.dump(self.dict, config, indent="")

    def HardUpdateJSON(self,newconfig):
        """Quick&Dirty Solution for updating internal JSON quickly"""
        self.dict=newconfig

    def GetURLPrefix(self):
        """Read URLPrefix in config"""
        assert ("URLPrefix" in self.dict), "URLPrefix key is missing in {} !".format(self.filename)
        
        URLPrefix = self.dict["URLPrefix"]    
        #Check to see that it's valid
        assert (URLPrefix!=""), "Please specify the URLPrefix for your target in {}".format(self.filename)    
        return URLPrefix

    def GetURLSuffix(self):
        """Read URLSuffix in config"""
        assert ("URLSuffix" in self.dict), "URLSuffix key is missing in {} !".format(self.filename)
        
        URLSuffix = self.dict["URLSuffix"]        
        #URLSuffix CAN be empty
        #assert (URLSuffix!=""), "Please specify the URLPrefix for your target in {}".format(self.filename)
        return URLSuffix

    def GetidCount(self):
        """Read idCount if found in config"""
        if "SiteInfo" in self.dict:
            return self.dict["SiteInfo"].get("idCount")
        return None