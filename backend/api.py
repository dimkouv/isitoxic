from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
import pickle
from utilities import clean

columns = ["toxic", "severe_toxic", "obscene",
           "threat", "insult", "identity_hate"]

def load_classifiers():
    classifiers = {}    
    for c in columns:
        filename = "./data/%s_classifier.sav" % (c)
        classifiers[c] = pickle.load(open(filename, "rb"))
    return classifiers


def load_vectorizer():
    return pickle.load(open("./data/vectorizer.sav", "rb"))


application = Flask(__name__)
CORS(application)
application.debug = True

classifiers = load_classifiers()
vectorizer = load_vectorizer()


@application.route("/")
def hello():
    return jsonify({
        "msg": "hello friend"
    })


@application.route("/predict/<msg>")
def predict(msg):
    predictions = {}
    test_vector = vectorizer.transform([clean(msg)])
    for c in columns:
        predictions[c] = classifiers[c].predict_proba(test_vector)[:,-1][0]
    return jsonify(predictions)

if __name__ == "__main__":
    application.run(host="0.0.0.0")
