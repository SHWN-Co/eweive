from flask import Flask, render_template, request, url_for, redirect, session, flash # (once we start creating html pages)
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruhmoment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eweive.db'
Bootstrap(app)
db = SQLAlchemy(app)
 
class User(db.Model, UserMixin):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    user_type = db.Column(db.String(10), nullable = False)
    phone_number = db.Column(db.String(100))
    cc_number = db.Column(db.String(100))
    email = db.Column(db.String(50), nullable = False, unique = True)
    def get_id(self):
        return self.id
 
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
 
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    email = StringField('email', validators=[InputRequired(), Length(min = 8, max = 80)])


# use python -m flask to run the app in VSCode
@app.route("/", methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@app.route('/OUApplication', methods = ['GET', 'POST'])
def OUApplication():
    return render_template("OUApplication.html")

@app.route("/login")
def login():
    form = LoginForm()
    return "login"
 
@app.route("/signup")
def signup():
    form = RegisterForm()
    return "signup"

@app.route("/homepage/<name>") 
def hello_there(name = None):
    return render_template(
        "homepage.html",
        name=name,
        date=datetime.now()
    )

@app.route("/item")
def itemPage():
    return render_template(
        "item.html",
        image_address="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title="Vincent Van Gogh Replica Painting Sunflowers",
        seller_id="342",
        end_date="December 14, 2022",
        highest_bid="$100.00",
        item_description="Van Gogh’s paintings of Sunflowers are among his most famous. He did them in Arles, in the south of France, in 1888 and 1889. Vincent painted a total of five large canvases with sunflowers in a vase, with three shades of yellow ‘and nothing else’. In this way, he demonstrated that it was possible to create an image with numerous variations of a single colour, without any loss of eloquence.")

@app.route("/report-item")
def reportPage():
    return render_template(
        "reportPage.html"
    )
