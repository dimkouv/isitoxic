# isitoxic
Check if a text is toxic. Toxic text contains insults, bruises, etc...  


## Description
`isitoxic.ipynb` contains my entry for

<a href="https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge">Toxic Comment Classification Challenge</a> by <a href="https://www.kaggle.com/jigsaw-team">Jigsaw</a>.


Using that notebook I implemented a simple API which predicts whether a text is toxic or not, based on a pre-trained stored classifier.

Furthermore a created a simple frontend that communicates with that API.


## Installation - Usage
First you need to get the train data from https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/download/train.csv.zip

After downloading extract and place `train.csv` in `./backend/data/`

Make sure all python dependencies are installed.
```bash
pip install -r ./backend/requirements.txt
```

Train the classifiers
```bash
cd backend
python3 train.py
```

Start backend
```bash
cd backend
python3 api.py
```

Test using curl or by opening `frontend/index.html`
```bash
# tested text is 'i am going to kill you'
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET 'http://localhost:5000/predict/i%20am%20going%20to%20kill%20you'
```
After running the command above you should get the following results, or at least results that mark the given string as a threat.
```json
{
  "identity_hate": 0.02882502394102831,
  "insult": 0.0300437672990749,
  "obscene": 0.19505636456788666,
  "severe_toxic": 0.18763813854270964,
  "threat": 0.9999940122445997,
  "toxic": 0.9976743329838031
}
```
