# -*- coding: utf-8 -*-
"""
This module contains common functions used
in the various readability calculations.

Wim Muskee, 2012-2013
wimmuskee@gmail.com

License: GPL-2
"""
from __future__ import division

def getTextScores(text, locale='en_GB', simplewordlist=[], smoggy=False):
    """
    Calculates several text scores based on a piece of text.
    A custom locale can be provided for the hyphenator, which
    maps to a Myspell hyphenator dictionary.
    The simple word list should be provided in lower case.
    """
    from nltk.tokenize import sent_tokenize
    from hyphenator import Hyphenator
    import re

    hyphenator = Hyphenator("/usr/share/myspell/hyph_" + locale + ".dic")
    scores = {
              'sent_count': 0,              # nr of sentences
              'word_count': 0,              # nr of words
              'letter_count':0,             # nr of characters in words (no spaces)
              'syll_count': 0,              # nr of syllables
              'polysyllword_count': 0,      # nr of polysyllables (words with more than 3 syllables)
              'simpleword_count': 0,        # nr of simplewords (depends on provided list)
              'sentlen_average': 0,         # words per sentence
              'wordlen_average': 0,         # syllables per word
              'wordletter_average': 0,      # letters per word
              'wordsent_average': 0         # sentences per word
              }

    sentences = sent_tokenize(text)
    sent_count = len(sentences)  # don't assign this to scores, as sentences may need to be recalculated
    if smoggy and sent_count > 30:  # see http://webpages.charter.net/ghal/SMOG_Readability_Formula_G._Harry_McLaughlin_%281969%29.pdf
        # get a sample of 10 sentences from the beginning, middle and the end of the text
        sentences = sentences[:10] + sentences[int(sent_count/2) -5:5+ int(sent_count/2)] + sentences[-10:]
    scores['sent_count'] = len(sentences)

    for s in sentences:
        words = re.findall(r'\w+', s.decode('utf8'), flags = re.UNICODE)
        scores['word_count'] = scores['word_count'] + len(words)

        for w in words:
            syllables_count = hyphenator.inserted(w).count('-') + 1
            scores['letter_count'] = scores['letter_count'] + len(w)
            scores['syll_count'] = scores['syll_count'] + syllables_count

            if syllables_count > 2:
                scores['polysyllword_count'] = scores['polysyllword_count'] + 1

            if simplewordlist:
                if w.lower() in simplewordlist:
                    scores['simpleword_count'] = scores['simpleword_count'] + 1


    scores['sentlen_average'] = scores['word_count'] / scores['sent_count']
    scores['wordlen_average'] = scores['syll_count'] / scores['word_count']
    scores['wordletter_average'] = scores['letter_count'] / scores['word_count']
    scores['wordsent_average'] = scores['sent_count'] / scores['word_count']
    return scores


def getMinimumAgeFromUsGrade(us_grade):
    """
    The age has a linear relation with the grade.
    http://en.wikipedia.org/wiki/Education_in_the_United_States#School_grades
    """
    return int(round(us_grade + 5))
