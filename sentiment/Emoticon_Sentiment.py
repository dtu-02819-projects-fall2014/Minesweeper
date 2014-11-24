"""
This class provides a binary sentiment analyzer (1 means positive, -1 means negative). 
It is autmatically created using emoticons from thousands of comments. 

Example:
    S=Emoticon_Sentiment("output.txt")
    S.read_base_comments()
    S.train_classifier(S.parse_comments())
    S.predict("This is aweful. I hate it!")

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

from pattern.vector import Document, NB
from pattern.db import csv
import HTMLParser, re, string,json
from nltk import word_tokenize
from nltk.corpus import stopwords


class Emoticon_Sentiment:
    """
    This class provides a binary sentiment analyzer (1 means positive, -1 means negative). 
    It is autmatically created using emoticons from thousands of comments. 
    """

    
    def __init__(self,basefile):
        """
        Args:
          basefile (str): The location of the comments file that should serve as the basis for the classifier.
        """
        self.base = basefile
        self.comments = []
        self.nb=NB()
        self.stop=stopwords.words('english')
        self.positive=[':-)', ':)', ':D' ,':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':っ)',':-D', '8-D', '8D', 
       'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', 'B^D',':-))',':*', ':^*',';-)', ';)', '*-)', '*)', ';-]'
       ';]', ';D', ';^)']
        self.negative=['>:[', ':-(' ,':(' , ':-c', ':c' ,':-<',  ':っC', ':<', ':-[', ':[' ,':{',':-||', ':@', '>:(','D:<', 'D:',
          'D8', 'D;', 'D=', 'DX', 'v.v','>:)', '>;)' ,'>:-)','}:-)' ,'}:)', '3:-)', '3:)',':-###..', ':###..',
          '>:/', ':-/', ':-.', ':/']
        
        
        
    def read_base_comments(self):
        """
        Reads the file that loads the comments that serve as the base for the classifier.

        Returns:
          list: list of comments from the text file
        """
        f = open(self.base, 'r')
        self.comments=json.load(f)
        f.close()
        return self.comments
    
    
    
    def preprocess(self,comment):   
        """
        Takes a comment and pre-processes it (all to lowercase, remove links, delete punctuation, remove stopwords and numbers)
        
        Args:
          comment (str): The text string to be processed

        Returns:
          str: the processed text string
        """
        h = HTMLParser.HTMLParser()
        text=h.unescape(comment.lower())
        link=r'http:\/\/.*[\r\n]*'
        p=re.compile(   r"(\b(?:(?:https?|ftp|file)://|www\.|ftp\.)[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|])"   )
        text=re.sub(p, '', text)
        exclude = set(string.punctuation)
        tokens=nltk.word_tokenize(text)
        cleaned=[token for token in tokens if token not in exclude]        
        text=' '.join([w.encode('ascii',errors='ignore') for w in cleaned if w.lower() not in self.stop and not w.isdigit()])    
        return text
    
    
    
    def parse_comments(self):
        """
        Parses a list of comments, by searching for emoticons. Once an emoticon is found, it flags it positive or negative. 
        With multiple finds, it sums their value; neutrals are thrown out.

        Returns:
          list: 2-dimensional list of parsed comments and their corresponding flags
        """
        extended_comments = [[self.comments[i],0, False] for i in range(len(self.comments))]
        
        #loop through comments and search for emoticons: +1 if positive, -1 if negative, and remove emoticons from text
        for comment in extended_comments:
    
            flagged=False
                 
            for n in negative:
                if comment[0].encode('utf-8').find(n)>-1:
                    comment[1]=comment[1]-1
                    comment[0]=comment[0].replace(n, '')
                    comment[2]=True
                    
            for p in positive:
                if comment[0].encode('utf-8').find(p)>-1:
                    
                    comment[1]=comment[1]+1
                    comment[0]=comment[0].replace(p, '')
                    comment[2]=True
        
        #throw out comments that have no emoticons
        parsed_comments=[[comment[0],comment[1]] for comment in extended_comments if comment[2]==True]
        
        #normalize the values by converting all positives (1,2,3,etc) to 1, and all negatives (-1,-2,-3 etc) to -1
        for item in parsed_comments:
            if item[1]>1:
                item[1]=1
            elif item[1]<-1:
                item[1]=-1
                
        #throw out neutrals
        parsed_comments=[[self.preprocess(i[0]),i[1]] for i in parsed_comments if i[1]!=0]
        
        return parsed_comments
    
    def train_classifier(self, comments):
        """
        takes the flagged comments and trains a Naive Bayes classifier
        
        Args:
          comments (list): The list of flagged comments to be trained
        """
        shuffle(comments)        
        
        for comment in comments:
            v = Document(comment[0], type=int(comment[1])) 
            self.nb.train(v)
            
    def predict(self, text):
        """
        Takes a comment and makes a sentiment prediction
        
        Args:
          text (str): The text string to be analyzed for sentiment

        Returns:
          int: 1 if positive sentiment, -1 if negative
        """
        return self.nb.classify(text)