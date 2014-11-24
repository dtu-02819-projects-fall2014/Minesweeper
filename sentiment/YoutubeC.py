"""
This class provides access to the comments of a given Youtube video.

Example:
    url="https://www.youtube.com/watch?v=5euHa8YMMgk"    
    Y = YoutubeC(url)
    Y.get_comments()
    Y.write_comments_to_file()

Created by Robert Gutke / robertgutke@hotmail.com / December 2014

Licensed under the MIT License:
Copyright (c) 2014, Robert Gutke
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import requests
import urlparse
import simplejson

class YoutubeC:
    """
    Provides access to the comments of a given Youtube video.
    """
    
    def __init__(self,url):
        """
        Args:
          url (str): The youtube video to be analyzed (as copied from the browser url field)
        """
        self.url = url
        self.video = urlparse.parse_qs(urlparse.urlparse(url).query)["v"][0]
        self.comments = []
    
    def write_comments_to_file(self):
        """
        Writes the list of comments to a json file
        """
        vs=self.video+'.json'
        f = open(vs, 'w')
        simplejson.dump(self.comments, f)
        f.close()
        
    def get_comments(self):
        """
        Takes the url of the youtube video and sends a http request via the youtube API. From the response, it
        takes the comments and the next link and sends it again to the Youtube API. This is repeated until no more
        next links are available. The reason for this iterative approach is the fact that Youtube only allows you
        to get 50 comments at a time.
        
        Returns:
          list: list of comments for a Youtube video
        """        
        next_page="http://gdata.youtube.com/feeds/api/videos/"+ self.video +"/comments?orderby=published&start-index=1&max-results=50&alt=json"
        comments=[]    
        
        while (next_page!=None):
            
            response=requests.get(next_page)    
            
            if response.status_code==200:
                
                # extract the json data from the response
                data = json.loads(response.text)            
                
                # get the link for the next resultpage
                if len(data['feed']['link'])>3:
                    next_page = data['feed']['link'][3]['href']
                else:
                    next_page = None
                        
                # extract the comments
                for entry in data['feed']['entry']:
                    self.comments.append(entry['content']['$t'])
               
            else:
                return self.comments
                
        return self.comments