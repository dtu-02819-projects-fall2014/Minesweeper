# [Minesweeper](https://github.com/MiningPythonGroup/Minesweeper)
## Tool to analyse the sentiment of youtube comments in Python


### I. Authors:
* André Castro Lundin

* Jakob Okkels

* Robert Gutke

Developed for the course of:

02819 Data mining using Python - Technical University of Denmark

### II. Description:
Classes:

* `YoutubeC.py` downloads all the Youtube comments for a video

* `Sentiment_analysis.py` finds the sentiment for a file with all the comments

* `Emoticon_Sentiment.py` provides a binary sentiment analyzer (1 = positive, -1 = negative)

### III. Word lists used:
- [AFINN list](http://neuro.imm.dtu.dk/wiki/AFINN)

- [MIT list](http://goo.gl/01A0iw)

#### 1. Demo of Sentiment analysis:

Process the data:

`import sentiment.Sentiment_analysis as senti`

`my_sent = Sentiment_analysis()`

`mit, afinn, positivecount, negativecount, sentimentlist1, sentimentlist2, sentimentlist3, emoticon = my_sent.get_sentiment_values('path_to_comments_file')`

Returns 
- sentiment values of MIT word list (mit), AFINN word list (afinn), emoticon classifier (emoticon)
- Word counters for possible word cloud (most common negative words and most common positive words)
- Lists of sentiment values for making a plot.

Print the results:

`print "MIT score: ", mit`

`print "AFINN score: ", afinn`

`print "Most common positive words: ", positivecount.most_common()[:10]`

`print "Most common negative words: ", negativecount.most_common()[:10]`

Returns something like:

`MIT score:  -1.40462962963`

`AFINN score:  -3.38888888889`

`Most common positive words:  [(u'god', 2), (u'eggs', 2), (u'sea', 1), (u'cattle', 1)]`

`Most common negative words:  [(u'kill', 4), (u'bitch', 4), (u'fat', 3), (u'fire', 2), (u'dead', 2), (u'fucking', 2), (u"can't sing", 2), (u'prison', 2), (u'yuck', 1), (u'monster', 1)]`

Make a plot of the sentiment as a function of time:

`my_sent.plot_of_comments(sentimentlist1, sentimentlist2, sentimentlist3, normalization=100, x_size=10, y_size=10, name_video="lol")`

The parameters are the 3 sentiment lists and (OPTIONAL):
- Normalization: Makes the lines smoother, though reduces the peaks. Suggested values between 10-1000
- x_size and y_size: Size of the image saved in directory
- name_video: Name for the graph file.

![alt text](http://i.imgur.com/951PSfU.png "Plot sample. Ignore smoothness, as the normalization and size were left to default")

### III. Other
Add here

![alt text](http://upload.wikimedia.org/wikipedia/en/5/5c/Minesweeper_Icon.png "Not that kind of mine. Datamining...")
