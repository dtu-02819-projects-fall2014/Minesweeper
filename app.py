import os
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for
from sentiment.Sentiment_analysis import Sentiment_analysis
from sentiment.YoutubeC import YoutubeC
import urlparse
import nltk
import requests
import simplejson
import re

class Video:
    """Contains information about the video. Each video should have it's own instance of Video.    """

    def __init__(self, url):
        """initializes and stores data about the video

        Args:
          url (str): The url of the video
          id (str): The Youtube Video ID
          sentiment_values: List of sentiment values
          graph_image_path: Path to the image of the sentiment-graph
          """

        self.url = url
        self.id =  urlparse.parse_qs(urlparse.urlparse(self.url).query)["v"][0]
        self.sentiment_values = self.get_sentiment_values()
        self.create_graph_image()
        self.graph_image_path = "/images/graphs/" + self.id + ".png"
        self.get_youtube_information()


    def get_sentiment_values(self):
        """Return sentiment values by extracting youtube comments and process these in sentiment_analysis."""
        youtubeC = YoutubeC(self.url)
        youtubeC.get_comments()
        youtubeC.write_comments_to_file()
        sentiment_values = Sentiment_analysis().get_sentiment_values("tmp/" + self.id + ".json")
        return sentiment_values


    def create_graph_image(self):
        """Creates graph of """
        Sentiment_analysis().plot_of_comments(self.sentiment_values[4], self.sentiment_values[5], self.sentiment_values[6], name_video=self.id)


    def get_youtube_information(self):
        response = requests.get("https://gdata.youtube.com/feeds/api/videos/" + self.id + "?v=2&alt=json")

        if response.status_code == 200:
            data = simplejson.loads(response.text)
            self.name = data["entry"]["title"]["$t"]
            self.thumbnail_url = data["entry"]["media$group"]["media$thumbnail"][3]["url"]

app = Flask(__name__, static_url_path = "")
app.jinja_env.add_extension("jinja2.ext.with_")


def isYoutubeURL(url):
    youtube_regex = (
    r'(https?://)?(www\.)?'
    '(youtube|youtu|youtube-nocookie)\.(com|be)/'
    '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    #if youtube_regex_match:
    #    return youtube_regex_match.group(6)

    return youtube_regex_match

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/comparison")
def comparison():
    video_1_url = request.args.get("video_1_url", "")
    video_2_url = request.args.get("video_2_url", "")
    if isYoutubeURL(video_1_url) and isYoutubeURL(video_2_url):

        video_1 = Video(request.args.get("video_1_url"))
        video_2 = Video(request.args.get("video_2_url"))

        return render_template(
            "comparison.html",
            video_1 = video_1,
            video_2 = video_2
        )
    else:
        return render_template("index.html", error_message = "Error")

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host = "0.0.0.0", port = port)