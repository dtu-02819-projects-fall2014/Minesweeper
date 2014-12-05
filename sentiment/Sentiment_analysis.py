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
        world_list_positve = Counter()
        word_list_negative = Counter()

        DB, AF = self.get_word_lists()
        comments = self.open_comments(comment_file)
        sentiment_score_mit,
		world_list_positve,
		word_list_negative,
		comment_graph_list_mit = (
                                  self.get_sentiment_value(comments, DB,
                                                              world_list_positve,
                                                              word_list_negative))
        sentiment_score_afinn, world_list_positve, word_list_negative, comment_graph_list_afinn = self.get_sentiment_value(comments, AF,
                                                              world_list_positve,
                                                              word_list_negative)

        # implementation of emoticons
        S = emse.Emoticon_Sentiment("tests/samples/output.txt")
        S.read_base_comments()
        S.train_classifier(S.parse_comments())
        list_of_emoticons = []
        for comment in comments:
            list_of_emoticons.append(S.predict(comment))

        # return emoticon value
        emoticon_positives = 0
        emoticon_negatives = 0
        for value in list_of_emoticons:
            try:
                if  value > 0:
                    emoticon_positives += int(value)
                else:
                    emoticon_negatives += int(value)
            except TypeError:
                print "TypeError: No emoticons on train set"
#               pass

        if emoticon_negatives > emoticon_positives:
            emoticon_score = -1
        else:
            emoticon_score = 1

        return sentiment_score_mit, sentiment_score_afinn, world_list_positve, word_list_negative,\
               comment_graph_list_mit, comment_graph_list_afinn, list_of_emoticons, emoticon_score

    def normalize_data(self, list1, amount, normalization):
        """Tool to normalize the list of comments.

        This is useful to avoid too much noise
        with many peaks when there are many comments.
        """
        new_list = []
        temp = 0
        for item in range(len(list1)):
            if amount < normalization:
                new_list = list1
            else:
                for i in range(0, int(amount/normalization)):
                    try:
                       temp += list1[item+i]
                    except:
                       pass
                temp = temp / (int(amount/normalization)+1)
                new_list.append(temp)
        return new_list

    def plot_of_comments(self, comment_graph1, comment_graph2,
                         comment_graph3,
                         normalization=100, x_size=10, y_size=10,
                         name_video="test"):
        """Save png graph of the comment sentiment as a function of time."""
        amount = len(comment_graph1)

        # Normalize lists
        cg1 = self.normalize_data(comment_graph1, amount, normalization)
        cg2 = self.normalize_data(comment_graph2, amount, normalization)
        cg3 = self.normalize_data(comment_graph3, amount, normalization)

        # set size
        rcParams['figure.figsize'] = x_size, y_size

        # data
        plt.plot(cg1, color='b', label='MIT')
        plt.plot(cg2, color='g', label='AFINN')
        plt.plot(cg3, color='r', label='Emoticon')
        plt.ylabel('sentiment')
        plt.xlabel('comment')
        plt.legend()
        plt.rcParams.update({'font.size': 22})
        # make pretty
        plt.savefig("static/images/graphs/" + name_video + ".png",bbox_inches='tight', transparent=True)
        plt.close()