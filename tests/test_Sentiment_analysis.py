# testing of sentiment class

import sentiment.Sentiment_analysis as senti
import nltk

my_sent = senti.Sentiment_analysis()


def test_if_word_lists_are_there():
    """Test that everything is ok with word lists."""
    a, b = my_sent.get_word_lists()
    assert len(a) == 3634
    assert len(b) == 2472


def test_sentiment_with_negative_file():
    """Testing a negative comment file made by us."""
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/negtest.txt')
    assert mi < -1
    assert af < -1


def test_sentiment_with_negative_file2():
    """Testing a negative comment file from youtube."""
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/football.txt')
    assert mi < -1
    assert af < -1


def test_sentiment_with_positive_file():
    """Testing a positive comment file from youtube."""
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/haloween.txt')
    assert mi > 1
    assert af > 1


def test_sentiment_with_neutral_file():
    """Testing a neutral comment file from youtube."""
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/hoi4.txt')
    assert mi < 1.5 and mi > -1.5
    assert af < 1.5 and af > -1.5


def test_sentiment_with_neutral_file2():
    """Testing a neutral comment file from youtube."""
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/double.txt')
    assert mi < 1.5 and mi > -1.5
    assert af < 1.5 and af > -1.5


def test_sentiment_with_enormous_file():
    """Testing a neutral comment file from youtube.

    WARNING!!!!! THIS TEST TAKES 5+ MINUTES,
    DUE TO HALF A MILLION COMMENTS.
    """
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/output.txt')
    assert mi < 3 and mi > -3
    assert af < 3 and af > -3


def test_plot_of_sentiment():
    """Testing the plot thing."""
    mi, af, po, ne, cg1, cg2, cg3, c = \
    my_sent.get_sentiment_values('tests/samples/output.txt')
    my_sent.plot_of_comments(cg1, cg2, cg3, normalization=100,
                             x_size=10, y_size=10, name_video="lol")
