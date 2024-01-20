from operator import methodcaller

from flask import Flask,request
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle

app = Flask(__name__)

@app.route("/train")
def train():
    try:
        df = pd.read_excel("False Alarm Cases.xlsx")
        x = df.iloc[:, 1:7]
        y = df["Spuriosity Index(0/1)"]
        logr = LogisticRegression()
        logr.fit(x, y)
        with open("train.pkl", "wb") as file:
            pickle.dump(logr, file)
        return "Model trained successfully"
    except:
        return "There is some error"

@app.route("/test",methods= ["POST"])
def test():
    data = request.get_json()
    return [data["Ambient Temperature"],
                                 data["Calibration"],
                                 data["Unwanted substance deposition"],
                                 data["Humidity"],
                                 data["H2S Content"],
                                 data["detected by"]]

    '''train_data = pickle.load("train.pkl")
    y_pred = train_data.predict([data["Ambient Temperature"],
                                 data["Calibration"],
                                 data["Unwanted substance deposition"],
                                 data["Humidity"],
                                 data["H2S Content"],
                                 data["detected by"]]) 
    if y_pred == 1:
        return "False Alarm"
    else:
        return "True Alarm" '''


app.run(port=5000)