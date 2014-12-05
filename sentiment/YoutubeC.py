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
"""


import requests
import urlparse
import simplejson


class YoutubeC:

    """Provides access to the comments of a given Youtube video."""

    def __init__(self, url):
        """
        Initialize the Youtube Comment extractor.

        Args:
          url (str): The youtube video to be analyzed (as copied from the
          browser url field)
        """
        self.url = url
        self.video = urlparse.parse_qs(urlparse.urlparse(url).query)["v"][0]
        self.comments = []

    def write_comments_to_file(self):
        """Write the list of comments to a json file."""
        vs = "tmp/" + self.video + ".json"
        f = open(vs, 'w')
        simplejson.dump(self.comments, f)
        f.close()

    def get_comments(self):
        """
        Get the comments of a youtube video.

        Take the url of the youtube video and sends a http request via the
        youtube API. From the response, it takes the comments and the next
        link and sends it again to the Youtube API. This is repeated until
        no more next links are available. The reason for this iterative
        approach is the fact that Youtube only allows you to get 50 comments
        at a time.

        Returns:
          list: list of comments for a Youtube video
        """
        next_page = ("http://gdata.youtube.com/feeds/api/videos/"
                     + self.video
                     + "/comments?orderby=published&start-index=1"
                     + "&max-results=50&alt=json")

        while (next_page is not None):

            response = requests.get(next_page)

            if response.status_code == 200:

                # extract the json data from the response
                data = simplejson.loads(response.text)

                # get the link for the next resultpage
                if len(data['feed']['link']) > 3:
                    next_page = data['feed']['link'][3]['href']
                else:
                    next_page = None

                # extract the comments
                for entry in data['feed']['entry']:
                    self.comments.append(entry['content']['$t'])

            else:
                return self.comments

        return self.comments
