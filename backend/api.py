from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from test import get_predictions

app = Flask(__name__)
CORS(app)
app.debug = True

@app.route("/")
def hello():
    return jsonify({
        "msg": "hello friend"
    })

@app.route("/predict/<msg>")
def predict(msg):
    return jsonify(get_predictions(msg))
