'''
Created on Jun 2, 2017

@author: Jose
'''
from src.net.AtlassianClient import AtlassianClient
import src.utils.Utilities

@ src.utils.Utilities.singleton
class MyClass(AtlassianClient):
    '''
    classdocs
    '''
    
    authRequest = "/rest-service/auth-v1/login"

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def getAuthToken(self):
        '''
        Get Rest API Token Auth 
        '''
        global authRequest
        self.executeRequest('GET', authRequest)
    
  