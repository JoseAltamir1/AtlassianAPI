'''
Created on Jun 2, 2017

@author: Jose
'''
import base64
import json
from multiprocessing.pool import ThreadPool

from src.Jira.Issue import Issue
from src.net.AtlassianClient import AtlassianClient
import src.utils.Utilities

@ src.utils.Utilities.singleton
class JiraClient(AtlassianClient):
    '''
    classdocs
    '''

    def __init__(self, host):
        '''
        Constructor
        '''
        super(JiraClient, self).__init__(host)
    
    def generateKey(self):
        '''
        Generate Basic Auth Key
        '''
        authStr = "{}:{}".format(super(JiraClient, self).__userName, super(JiraClient, self).__passWord)
        self.__encodedPass = base64.b64decode(authStr)
                
    def executeRequest(self, requestType, request):
        '''
        Execute Jira Request
        '''        
        # Set header with auth and excepted response type
        header = {'Authorization' : self.__encodedPass, 'Accept' : 'application/json'}
        # Run parent request executer        
        return super(JiraClient, self).executeRequest(self, requestType, request, header=header)
    
    def getIssue(self, issueID):
        '''
        Get issue data from Jira
        '''
        # Format Jira issue Rest API call
        issueQuery = '/rest/api/2/issue/{}'.format(issueID)
        # Execute request
        response = self.executeRequest('GET', issueQuery)
        # Return issue object
        return Issue(issueID, response)
    
    def runJQL(self, query):
        '''
        Execute JQL
        '''
        def execJQL(jqlQuery):
            # Execute JQL request        
            firstResponse = self.executeRequest('GET', jqlQuery)
            # return response in JSON map
            return json.load(firstResponse)
        
        # Define max results per query
        maxResults = 500
        # Format JQL Rest API call
        jqlQuery = '/rest/api/2/search?={}&startAt={}&maxResults={}'
        # Execute JQL request        
        firstResponse = execJQL(jqlQuery.format(query, 0, maxResults))
        # Get total number of responses from the JQL 
        totalCount = float(firstResponse.get('total'))
        # Create pool with 10 threads 
        pool = ThreadPool(10)
        # Feed list of JQLs to execute
        results = pool.map(execJQL, [jqlQuery.format(query, i * maxResults, maxResults) for i in xrange(maxResults, totalCount, maxResults)])
        # Close pool
        pool.close()
        # Wait for all threads to finish
        pool.join()    
        
        # Add first response to loop through all responses
        results.append(firstResponse)
        
        listOfIssues = []
        for response in results:
            for issue in response.get('issue'):
                listOfIssues.append(Issue(issue.get('id'), json.dump(issue)))
        
        return listOfIssues
                