from __future__ import division
import nltk, re, pprint
from collections import Counter
from nltk.corpus import stopwords
import json
import math
import simplejson

class sentiment_analysis:
    """Returns if a group of comments are positive, neutral or negative"""
    
    def __init__(self):
        self.data = []
        self.description = "Returns if a group of comments are positive, neutral or negative"
        self.author = "André, Robert, Jakob"
        
    def get_word_lists(self):
               
        #load sentiment DB and steps http://www.plosone.org/article/info:doi/10.1371/journal.pone.0026752#pone.0026752.s001
        sentimentDB = {}
        sentimentfile = json.loads(open('sentiment.json').read())
        for k,i in sentimentfile.iteritems():
            if float(i)>6 or float(i)<4:
                sentimentDB[k] = (float(i) - 5)
        
        #Implementation of AFINN list
        sentimentAF = {}
        sentimentfile2 = json.loads(open('sentimentAF.json').read())
        for item in sentimentfile2:
            try:
                sentimentAF[item[0]] = float(item[-1])
            except ValueError:
                print 'Unexpected line: {!r}'.format(item)
        return sentimentDB, sentimentAF
    
    def open_comments(self, filename):
        f = open(filename, 'r')
        temp1=simplejson.load(f)
        f.close()
        temp = list(set(temp1))
        return temp
        
    def tokenize(self, comments):
        final = []
        token_comments = comments.split()
        stop = stopwords.words('english')
        # LATER!! add append title words herE
        
        for item in token_comments:
            if item.lower() not in stop:
                if len(item) > 2:
                    item1 = re.sub('!', '', item) #removing marks until used REVISE!
                    item2 = re.sub(u'\ufeff', '', item1)
                    final.append(item2.lower())
        return final
    
    def get_sentiment_value(self, comments, sentlist, pos, neg): #sentlist: sentimentDB or sentimentAF
        final = 0
        final_ammount = 0
        sentiment = 0
        pos_list = []
        neg_list = []
        for comment in comments:
            #print comment #for debugging
            total = 0
            number = 0
            value = 0
            invert = False
            word = ""
            test_list = ['not', 'cant', 'isnt', "can't", "isn't", "cannot", "couldnt", 
                         "wouldnt", "couldn't", "wouldn't", "doesnt", "doesn't", "don't", "dont"] #Inverting words
            temp_list = self.tokenize(comment)
            #print temp_list #for debugging
            
            for item in temp_list:
                if item.lower() in test_list:
                        invert = True
                        #print "inverted", item.lower() #for debugging
                        for k,i in sentlist.iteritems():
                            if item.lower() == k:
                                value = i
                                word = k
                            else:
                                value = 0
                else:
                    for k,i in sentlist.iteritems():
                        if item.lower() == k:
                            if invert == True:
                                total = total - i
                                number = number + 1
                                invert = False
                                #print k, " inverted: ", -i #for debugging
                                if i < 0:
                                    pos_list.append(word + " " + k)
                                else:
                                    neg_list.append(word + " " + k)
                            else:
                                total = total + i
                                number = number + 1
                                #print k, i #for debugging
                                if i < 0:
                                    neg_list.append(k)
                                else:
                                    pos_list.append(k)
                    if invert == True:
                        invert = False
                        #print "next word unknown", value #for debugging
                        if value < 0 and len(word) > 1: #remove one letter or less words
                            neg_list.append(word)
                            total = total + value
                            number = number + 1
                        elif value > 0 and len(word) > 1:
                            pos_list.append(word)
                            total = total + value
                            number = number + 1
                        value = 0
                        word = ""
            if number != 0 and total != 0:
                final = final + (total/number)
                final_ammount = final_ammount + 1
                #print "comment score: ", total/number #for debugging
        
        for w in [pos_list]:
            pos.update(w)
        for w in [neg_list]:
            neg.update(w)
        sentiment = final / final_ammount
        return sentiment, pos, neg
    
    def get_sentiment_values(self, comment_file):
        #Counters for word lists
        positive = Counter()
        negative = Counter()
        
        DB, AF = self.get_word_lists()
        comments = self.open_comments(comment_file)
        a, positive, negative = self.get_sentiment_value(comments, DB, positive, negative)
        b, positive, negative = self.get_sentiment_value(comments, AF, positive, negative)
        #print "MIT Score: ", a, "AFINN Score: ", b
        #print "Top positive: ", positive.most_common()[:10] 
        #print "Top negative: ", negative.most_common()[:10] 
        return a, b, positive, negative



my_sent = sentiment_analysis()
mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('videos/negtest.txt')



print "MIT score: ", mit
print "AFINN score: ", afinn
print "Most common positive words: ", positivecount.most_common()[:10] 
print "Most common negative words: ", negativecount.most_common()[:10] 
if mit>0.5 and afinn>0.5:
    print "Positive comments "
elif mit<-0.5 and afinn<-0.5:
    print "Negative comments "
else:
    print "Neutral comments "



"""The following hasn't been implemented properly yet. Regarding word cloud"""



import os
import collections
import re
#from wordcloud import WordCloud
import wordcloud
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

textPath = 'textFile/'
pngPath = 'wordCloud/'

myWC = wordcloud.WordCloud()

def genWordCloud(filename):
    count = filename
    #words = myWC.fit_words(count, width=500, height=500)
    words = myWC.fit_words(count)
    myWC.draw(words, pngPath + os.path.splitext(filename)[0] + '.png', width=500, height=500, scale=1)
    return 'Cloud generated for {}'.format(filename)

if __name__ == '__main__':
    for filename in os.listdir(textPath):
        print genWordCloud(filename)




list_of_tuples = [(str(k), float(v)) for k, v in positivecount.most_common()[:10]]

#for x in list_of_tuples:
#    print x[0], x[1]

#genWordCloud(list_of_tuples)




