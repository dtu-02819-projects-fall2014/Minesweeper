# testing of sentiment class

import sentiment.Sentiment_analysis as senti
import nltk

my_sent = senti.Sentiment_analysis()

def test_if_word_lists_are_there():
    """Test that everything is ok with word lists"""
    a, b = my_sent.get_word_lists()
    assert len(a) == 3634
    assert len(b) == 2472
	
def test_sentiment_with_sample_file():
    """Testing a negative comment file"""
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('tests/samples/negtest.txt')
    assert mit < -1
    assert afinn < -1