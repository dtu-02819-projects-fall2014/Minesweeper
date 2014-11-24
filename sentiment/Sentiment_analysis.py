"""Contains the Sentiment_analysis class.

Used for assesing the sentiment of a group of strings.
"""
from __future__ import division
import re
from collections import Counter
from nltk.corpus import stopwords
import json
import simplejson


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
        sentimentfile = json.loads(open('sentiment.json').read())
        for k, i in sentimentfile.iteritems():
            if float(i) > 6 or float(i) < 4:
                sentimentDB[k] = (float(i) - 5)

        sentimentAF = {}
        sentimentfile2 = json.loads(open('sentimentAF.json').read())
        for item in sentimentfile2:
            try:
                sentimentAF[item[0]] = float(item[-1])
            except ValueError:
                print 'Unexpected line: {!r}'.format(item)
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
        for comment in comments:
            # print comment #for debugging
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
            # print temp_list #for debugging

            for item in temp_list:
                if item.lower() in test_list:
                        invert = True
                        # print "inverted", item.lower() #for debugging
                        for k, i in sentlist.iteritems():
                            if item.lower() == k:
                                value = i
                                word = k
                            else:
                                value = 0
                else:
                    for k, i in sentlist.iteritems():
                        if item.lower() == k:
                            if invert:
                                total = total - i
                                number += 1
                                invert = False
                                # print k, " inverted: ", -i #for debugging
                                if i < 0:
                                    pos_list.append(word + " " + k)
                                else:
                                    neg_list.append(word + " " + k)
                            else:
                                total += i
                                number += 1
                                # print k, i #for debugging
                                if i < 0:
                                    neg_list.append(k)
                                else:
                                    pos_list.append(k)
                    if invert:
                        invert = False
                        # print "next word unknown", value #for debugging
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
                # print "comment score: ", total/number #for debugging

        for w in [pos_list]:
            pos.update(w)
        for w in [neg_list]:
            neg.update(w)
        sentiment = final / final_ammount
        return sentiment, pos, neg

    def get_sentiment_values(self, comment_file):
        """Run get_sentiment for both word lists."""
        positive = Counter()
        negative = Counter()

        DB, AF = self.get_word_lists()
        comments = self.open_comments(comment_file)
        a, positive, negative = self.get_sentiment_value(comments, DB,
                                                         positive, negative)
        b, positive, negative = self.get_sentiment_value(comments, AF,
                                                         positive, negative)
        return a, b, positive, negative
