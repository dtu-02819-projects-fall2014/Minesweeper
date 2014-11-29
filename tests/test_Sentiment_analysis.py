# testing of sentiment class

import sentiment.Sentiment_analysis as senti
import nltk

my_sent = senti.Sentiment_analysis()

def test_if_word_lists_are_there():
    """Test that everything is ok with word lists"""
    a, b = my_sent.get_word_lists()
    assert len(a) == 3634
    assert len(b) == 2472

def test_sentiment_with_negative_file():
    """Testing a negative comment file made by us"""
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/negtest.txt')
    assert mit < -1
    assert afinn < -1

def test_sentiment_with_negative_file2():
    """Testing a negative comment file from youtube"""
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/football.txt')
    assert mit < -1
    assert afinn < -1

def test_sentiment_with_positive_file():
    """Testing a positive comment file from youtube"""
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/haloween.txt')
    assert mit > 1
    assert afinn > 1

def test_sentiment_with_neutral_file():
    """Testing a neutral comment file from youtube"""
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/hoi4.txt')
    assert mit < 1.5 and mit > -1.5
    assert afinn < 1.5 and afinn > -1.5

def test_sentiment_with_neutral_file2():
    """Testing a neutral comment file from youtube"""
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/double.txt')
    assert mit < 1.5 and mit > -1.5
    assert afinn < 1.5 and afinn > -1.5

def test_sentiment_with_enormous_file():
    """Testing a neutral comment file from youtube.

    WARNING!!!!! THIS TEST TAKES 5+ MINUTES, 
    DUE TO HALF A MILLION COMMENTS
    """
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/output.txt')
    assert mit < 3 and mit > -3
    assert afinn < 3 and afinn > -3