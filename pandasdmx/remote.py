# encoding: utf-8

import requests
from tempfile import SpooledTemporaryFile as STF
from contextlib import closing

    

class REST:
    """
    Query resources via REST
    """

    max_size = 2**24
    '''upper bound for in-memory temp file. Larger files will be spooled from disc'''
        
                             
    def get(self, url, fromfile = None, params = {}):
        '''Get SDMX message from REST service or local file
        
        Args:
        
            url(str): URL of the REST service without the query part
                If None, fromfile must be set. Default is None
            params(dict): will be appended as query part to the URL after a '?'  
            fromfile(str): path to SDMX file containing an SDMX message. 
                It will be passed on to the
                reader for parsing.
                
        Returns: 
            tuple: three objects:
            
                0. file-like object containing the SDMX message
                1. the complete URL, if any, including the query part
                   constructed from params
                2. the status code 
        
        Raises: 
            HTTPError if SDMX service responded with
                status code 401. Otherwise, the status code
                is returned
 '''
        if fromfile:
            # Load data from local file 
            source = open(fromfile, 'rb')
            final_url = status_code = None    
        else:
            source, final_url, status_code = self.request(url, params = params) 
        return source, final_url, status_code
         
    
    def request(self, url, params = {}):
        """
        Retrieve SDMX messages.
        If needed, override in subclasses to support other data providers.

        :param url: The URL of the message.
        :type url: str
        :return: the xml data as file-like object 
        """
        
        with closing(requests.get(url, params = params, 
                                  stream = True, timeout= 30.1)) as response:
            if response.status_code == requests.codes.OK:
                source = STF(max_size = self.max_size)
                for c in response.iter_content(chunk_size = 1000000):
                    source.write(c)
                source.seek(0)
            else:
                source = None
            code = int(response.status_code)
            if code == 401: raise requests.HTTPError() 
            return source, response.url, code