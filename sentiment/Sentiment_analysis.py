#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the Sentiment_analysis class.

Used for assesing the sentiment of a group of strings.
"""
from __future__ import division
import re
from collections import Counter
from nltk.corpus import stopwords
import json
import simplejson
import matplotlib.pyplot as plt
from pylab import rcParams
import sentiment.Emoticon_Sentiment as emse


class Sentiment_analysis:

    """Returns if a group of comments are positive, neutral or negative."""

    def __init__(self):
        """ ATM just includes the description and authors."""
        self.data = []
        self.description = "Finds sentiment value"
        self.author = "Andre Castro"

    def get_word_lists(self):
        """Load sentiment word lists.

        - MIT List (see http://goo.gl/01A0iw)
        - AFINN List
        Returns both lists.
        """
        sentimentDB = {}
        first = open('sentiment/sentiment.json')
        sentimentfile = json.loads(first.read())
        for k, i in sentimentfile.iteritems():
            if float(i) > 6 or float(i) < 4:
                sentimentDB[k] = (float(i) - 5)
        first.close()
        sentimentAF = {}
        second = open('sentiment/sentimentAF.json')
        sentimentfile2 = json.loads(second.read())
        for item in sentimentfile2:
            try:
                sentimentAF[item[0]] = float(item[-1])
            except ValueError:
                print 'Unexpected line: {!r}'.format(item)
        second.close()
        return sentimentDB, sentimentAF

    def open_comments(self, filename):
        """Load the file containing the youtube comments."""
        f = open(filename, 'r')
        temp1 = simplejson.load(f)
        f.close()
        temp = list(set(temp1))
        return temp

    def tokenize(self, comments):
        """Tokenize the imported youtube comments."""
        final = []
        token_comments = comments.split()
        stop = stopwords.words('english')

        for item in token_comments:
            if item.lower() not in stop:
                if len(item) > 2:
                    item1 = re.sub('!', '', item)
                    item2 = re.sub(u'\ufeff', '', item1)
                    final.append(item2.lower())
        return final

    def get_sentiment_value(self, comments, sentlist, pos, neg):
        """Return the sentiment values of a tokenized comments list.

        - sentlist: word list. Ex: sentimentDB or sentimentAF
        - Comments: Tokenized comments
        - pos, neg: Counters with most used positive and negative words.
        """
        final = 0
        final_ammount = 0
        sentiment = 0
        pos_list = []
        neg_list = []
        comment_graph = []
        for comment in comments:
            total = 0
            number = 0
            value = 0
            invert = False
            word = ""
            test_list = ['not', 'cant', 'isnt', "can't",
                         "isn't", "cannot", "couldnt", "wouldnt",
                         "couldn't", "wouldn't", "doesnt", "doesn't",
                         "don't", "dont"]  # Inverting words
            temp_list = self.tokenize(comment)

            for item in temp_list:
                if item.lower() in test_list:
                    invert = True
                    if item.lower() in sentlist:
                        value = sentlist[item.lower()]
                        word = item.lower()
                    else:
                        value = 0

                else:
                    if item.lower() in sentlist:
                        i = sentlist[item.lower()]
                        if invert:
                            total = total - i
                            number += 1
                            invert = False
                            if i < 0:
                                pos_list.append(word + " " + item.lower())
                            else:
                                neg_list.append(word + " " + item.lower())
                        else:
                            total += i
                            number += 1
                            if i < 0:
                                neg_list.append(item.lower())
                            else:
                                pos_list.append(item.lower())

                    if invert:
                        invert = False
                        if value < 0 and len(word) > 1:
                            neg_list.append(word)
                            total = total + value
                            number += 1
                        elif value > 0 and len(word) > 1:
                            pos_list.append(word)
                            total = total + value
                            number += 1
                        value = 0
                        word = ""
            if number != 0 and total != 0:
                final = final + (total/number)
                final_ammount += 1
                comment_graph.append(total/number)
            else:
                comment_graph.append(0)

        for w in [pos_list]:
            pos.update(w)
        for w in [neg_list]:
            neg.update(w)
        if final != 0 and final_ammount != 0:
            sentiment = final / final_ammount
        else:
            sentiment = 0
        return sentiment, pos, neg, comment_graph

    def get_sentiment_values(self, comment_file):
        """Run get_sentiment for both word lists."""
        positive = Counter()
        negative = Counter()

        DB, AF = self.get_word_lists()
        comments = self.open_comments(comment_file)
        a, positive, negative, cg1 = self.get_sentiment_value(comments, DB,
                                                              positive,
                                                              negative)
        b, positive, negative, cg2 = self.get_sentiment_value(comments, AF,
                                                              positive,
                                                              negative)

        # implementation of emoticons
        S = emse.Emoticon_Sentiment(comment_file)
        S.read_base_comments()
        S.train_classifier(S.parse_comments())
        los = []
        for comment in comments:
            los.append(S.predict(comment))

        # return emoticon value
        c = 0
        for item in los:
            try:
               c += int(item)
            except TypeError:
                print "TypeError: No emoticons found"
#               pass
        c = c / len(los)
        return a, b, positive, negative, cg1, cg2, los, c

    def plot_of_comments(self, comment_graph1, comment_graph2,
                         comment_graph3,
                         normalization=100, x_size=10, y_size=10,
                         name_video="test"):
        """Save png graph of the comment sentiment as a function of time."""
        amount = len(comment_graph1)
        new_cg1 = []
        temp = 0
        for item in range(len(comment_graph1)):
            if amount < normalization:
                new_cg1 = comment_graph1
            else:
                for i in range(0, int(amount/normalization)):
                    try:
                        temp += comment_graph1[item+i]
                    except:
                        pass
                temp = temp / (int(amount/normalization)+1)
                new_cg1.append(temp)
                temp = 0

        new_cg2 = []
        for item in range(len(comment_graph2)):
            if amount < normalization:
                new_cg2 = comment_graph2
            else:
                for i in range(0, int(amount/normalization)):
                    try:
                        temp += comment_graph2[item+i]
                    except:
                        pass
                temp = temp / (int(amount/normalization)+1)
                new_cg2.append(temp)
                temp = 0

        new_cg3 = []
        for item in range(len(comment_graph3)):
            if amount < normalization:
                new_cg3 = comment_graph3
            else:
                for i in range(0, int(amount/normalization)):
                    try:
                        temp += comment_graph3[item+i]
                    except:
                        pass
                temp = temp / (int(amount/normalization)+1)
                new_cg3.append(temp)
                temp = 0

        # set size
        rcParams['figure.figsize'] = x_size, y_size

        # data
        plt.plot(new_cg1, color='b', label='MIT')
        plt.plot(new_cg2, color='g', label='AFINN')
        plt.plot(new_cg3, color='r', label='Emoticon')
        plt.ylabel('sentiment')
        plt.xlabel('comment')
        plt.legend()

        # make pretty
        plt.savefig(name_video + '.png')
