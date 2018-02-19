#!/usr/bin/python3
'''
This script has some utilities used from
both train.py and test.py
'''
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import re

def clean(text):
    lem = WordNetLemmatizer()
    stem = PorterStemmer()

    text = text.replace("\n", " ")
    text = " ".join([w for w in text.split() if len(w) < 25])
    text = " ".join(word_tokenize(text))
    text = re.sub(r"[^A-Za-z0-9']+", " ", text)
    text = " ".join([stem.stem(lem.lemmatize(word, "v"))
                     for word in text.split()])
    text = text.lower()

    rep = {
        "[f]+[u]+[c]+[k]+": "fuck",
        "fukc": "fuck",
        "fcuk": "fuck",
        "nlgga": "nigga"
    }
    regex = re.compile("(%s)" % "|".join(map(re.escape, rep.keys())))
    text = regex.sub(lambda mo: rep[mo.string[mo.start():mo.end()]], text)
    return text
