'''
Created on Jun 2, 2017

@author: Jose
'''

from urllib3 import HTTPSConnectionPool


class AtlassianClient(object):
    '''
    classdocs
    '''
    
    def __init__(self, host):
        '''
        Constructor
        '''
        self.__httpsPool = HTTPSConnectionPool(host)
    
    def executeRequest(self, requestType, request):
        response = self.__httpsPool.urlopen(requestType, request)
        
        if response.status == 200:
            return response
        return None
    
    