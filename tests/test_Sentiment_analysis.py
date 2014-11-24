# testing of sentiment class

import Sentiment_analysis

my_sent = Sentiment_analysis()

def test_if_word_lists_are_there():
    a, b = my_sent.get_word_lists()
    assert len(a) == 3634
    assert len(b) == 2472
	
def test_sentiment_with_sample_file():
    mit, afinn, positivecount, negativecount = my_sent.get_sentiment_values('samples/negtest.txt')
    assert mit < -1
	assert afinn < -1