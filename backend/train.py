#!/usr/bin/python3
'''
What this script does:
1. Reads train data
2. Creates and trains classifiers
3. Stores classifiers for usage from other apps
'''
import collections
import pandas as pd
import numpy as np
import pickle
from utilities import clean

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

train_data = pd.read_csv('./data/train.csv')
columns = ["toxic", "severe_toxic", "obscene",
           "threat", "insult", "identity_hate"]

values = {c: train_data[c] for c in columns}
texts = [clean(t) for t in train_data["comment_text"]]
del train_data

# remove duplicates
tmp = set([x for x, count in collections.Counter(texts).items() if count == 1])
tmp = [i for i, x in enumerate(texts) if x in tmp]
texts = [texts[i] for i in tmp]
for c in columns:
    values[c] = [values[c][i] for i in tmp]

# remove clean comments with length greater than 4000
# (we already have too much clean comments)
clean_ind = {}
for i in range(len(texts)):
    s = 0
    for c in columns:
        s += values[c][i]
    if s == 0:
        clean_ind[i] = True
tmp = [i for i, t in enumerate(texts) if not(i in clean_ind and len(t) > 4000)]
texts = [texts[i] for i in tmp]
for c in columns:
    values[c] = [values[c][i] for i in tmp]


# remove texts with length lower than 6
tmp = [i for i, text in enumerate(texts) if len(text) >= 5]
texts = [texts[i] for i in tmp]
for c in columns:
    values[c] = [values[c][i] for i in tmp]

vectorizer = TfidfVectorizer(
    max_df=0.80,
    ngram_range=(1, 2),
    smooth_idf=False,
    sublinear_tf=True
)
vectors = vectorizer.fit_transform(texts)


classifier = SGDClassifier(
    loss="log",
    penalty="l1",
    alpha=5**-8,
    max_iter=15,
    n_jobs=-1,
    random_state=42
)

for c in columns:
    classifier.fit(vectors, values[c])

    X_train, X_test, y_train, y_test = train_test_split(
        vectors,
        values[c],
        test_size=0.20,
        random_state=42
    )

    predictions = classifier.predict_proba(X_test)
    rauc = roc_auc_score(y_test, predictions[:, 1])
    print("%-20s" % (c+" | Rauc"), rauc)

    # save classifier
    filename = "./data/%s_classifier.sav" % (c)
    with open(filename, "wb") as f:
        pickle.dump(classifier, f)


# save vectorizer
with open("./data/vectorizer.sav", "wb") as f:
    pickle.dump(vectorizer, f)
