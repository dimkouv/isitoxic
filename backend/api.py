from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from test import get_predictions

application = Flask(__name__)
CORS(application)
application.debug = True

@application.route("/")
def hello():
    return jsonify({
        "msg": "hello friend"
    })

@application.route("/predict/<msg>")
def predict(msg):
    return jsonify(get_predictions(msg))

if __name__ == "__main__":
    application.run(host="0.0.0.0")

