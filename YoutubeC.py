import requests
import elementtree.ElementTree as ET

class YoutubeC:
    def __init__(self,video):
        self.video = video
        self.comments = []
        
    def get_comments(self):
        next_page="http://gdata.youtube.com/feeds/api/videos/"+ self.video +"/comments?orderby=published&start-index=1&max-results=50"   
        
        while (next_page!=None):
            
            response=requests.get(next_page)    
            
            if(response.ok):
                
                # extract the data from the response
                raw = response.text    
                root = ET.fromstring(raw.encode('utf-8'))
                
                # get the link for the next resultpage
                links = root.findall('{http://www.w3.org/2005/Atom}link')
                if(size(links)>3):
                    next_page = links[3].attrib.get("href")
                else:
                    next_page = None
                        
                # extract the comments
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    comment = entry.find('{http://www.w3.org/2005/Atom}content').text
                    if(comment!=None):
                        self.comments.append(comment)
                
            else:
                return self.comments
                
        return self.comments