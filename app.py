"""
Functions as a controller for the website.

Collects information from other classes.
and renders the website.
"""

import os
from flask import Flask, render_template, request
from sentiment.Sentiment_analysis import Sentiment_analysis
from sentiment.YoutubeC import YoutubeC
import urlparse
import requests
import simplejson
import re


class Video:

    """
    Contains information about the video.

    Collects information about the video, by extracting comments,
    and analysising the sentiment of them.
    Each video got it's own instance of Video
    """

    def __init__(self, url):
        """initialize and store data about the video.

        Args:
        url (str): The url of the video

        Variables:
        id (str): The Youtube Video ID
        sentiment_values: List of sentiment values
        graph_image_path: Path to the image of the sentiment-graph
        """
        self.url = url
        self.id = urlparse.parse_qs(urlparse.urlparse(self.url).query)["v"][0]
        self.sentiment_values = self.get_sentiment_values()
        self.create_graph_image()
        self.graph_image_path = "/images/graphs/" + self.id + ".png"
        self.get_youtube_information()

    def get_sentiment_values(self):
        """
        Return sentiment values by extracting youtube comments.

        Afterwards a sentiment analysis is performed.
        """
        youtube_comment_extractor = YoutubeC(self.url)
        youtube_comment_extractor.get_comments()
        youtube_comment_extractor.write_comments_to_file()
        sentiment_values = Sentiment_analysis() \
            .get_sentiment_values("tmp/" + self.id + ".json")
        return sentiment_values

    def create_graph_image(self):
        """
        Create "Sentiment Over Time" -graph.

        Creates the graph and saves it
        And saves the file as the videoid .png
        """
        Sentiment_analysis().plot_of_comments(self.sentiment_values[4],
                                              self.sentiment_values[5],
                                              self.sentiment_values[6],
                                              name_video=self.id,
                                              normalization=20)

    def get_youtube_information(self):
        """ Collect the youtube videos title and thumbnail."""
        response = requests.get(
            "https://gdata.youtube.com/feeds/api/videos/"
            + self.id + "?v=2&alt=json")
        if response.status_code == 200:
            data = simplejson.loads(response.text)
            self.name = data["entry"]["title"]["$t"]
            self.thumbnail_url = data["entry"][
                "media$group"]["media$thumbnail"][3]["url"]


app = Flask(__name__, static_url_path="")
app.jinja_env.add_extension("jinja2.ext.with_")


def is_youtube_url(url):
    """
    Return True or False depending on the URL is a youtube url or not.

    Args:
    url (str): the URL of the video to be examined.

    Returns:
    bool: True if youtube link is valid, otherwise False
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)

    return youtube_regex_match


@app.route("/")
def index():
    """Render Index Page."""
    return render_template("index.html")


@app.route("/comparison")
def comparison():
    """
    Create videos and rensers Comparison site.
    
    Create 2 instances of Video, checks whether they are valid links.
    If they are the comparison-page is rendered.
    Otherwise the index page is shown with an error message.

    Variables:
    video_1_url (str) and video_2_url (str):
        The user inputted strings of the URL for the Youtube Videos.
    """
    video_1_url = request.args.get("video_1_url", "")
    video_2_url = request.args.get("video_2_url", "")
    if is_youtube_url(video_1_url) and is_youtube_url(video_2_url):

        video_1 = Video(request.args.get("video_1_url"))
        video_2 = Video(request.args.get("video_2_url"))

        return render_template(
            "comparison.html",
            video_1=video_1,
            video_2=video_2
        )
    else:
        return render_template("index.html", error_message="Error")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
