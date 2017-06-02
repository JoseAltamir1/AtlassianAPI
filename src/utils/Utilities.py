'''
Created on Jun 2, 2017

@author: Jose
'''

import ConfigParser

def singleton(cls):
    instances = {}
    def getInstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
def loadIni():
    config = ConfigParser.ConfigParser()
    config.read("res\\AtlassianConfig.ini")
    return config