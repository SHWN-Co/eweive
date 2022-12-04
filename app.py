from flask import Flask, render_template, request, url_for, redirect, session # (once we start creating html pages)
from datetime import datetime

app = Flask(__name__)

# use python -m flask to run the app in VSCode
@app.route("/", methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@app.route('/OUApplication', methods = ['GET', 'POST'])
def OUApplication():
    return render_template("OUApplication.html")

@app.route("/homepage/<name>") 
def hello_there(name = None):
    return render_template(
        "homepage.html",
        name=name,
        date=datetime.now()
    )




