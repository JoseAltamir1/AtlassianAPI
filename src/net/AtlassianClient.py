'''
Created on Jun 2, 2017

@author: Jose
'''

from urllib3 import HTTPSConnectionPool


class AtlassianClient(object):
    '''
    classdocs
    '''
    
    def __init__(self, host, userName, passWord):
        '''
        Constructor
        '''
        self.__httpsPool = HTTPSConnectionPool(host)
        self.__userName = userName
        self.__passWord = passWord
    
    def executeRequest(self, requestType, request, header = None):
        response = self.__httpsPool.urlopen(requestType, request, header)
        
        if response.status == 200:
            return response
        return None
    
    