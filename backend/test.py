#!/usr/bin/python3
'''
What this script does:
1. Loads trained classifier and vectorizer
2. Cleans given text
3. Predicts
'''
import pickle
from utilities import clean

columns = ["toxic", "severe_toxic", "obscene",
           "threat", "insult", "identity_hate"]

def get_predictions(text):
    predictions = {}

    vectorizer = pickle.load(open("./data/vectorizer.sav", "rb"))

    test_vector = vectorizer.transform([clean(text)])
    
    for c in columns:
        filename = "./data/%s_classifier.sav" % (c)
        classifier = pickle.load(open(filename, "rb"))
        predictions[c] = classifier.predict_proba(test_vector)[:,-1][0]

    return predictions

