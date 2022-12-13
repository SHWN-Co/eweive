import enum
from flask import Flask, render_template, request, url_for, redirect, session, flash
from sqlalchemy import DateTime, Enum, ForeignKey, func, Integer # (once we start creating html pages)
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime, timedelta

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruhmoment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'eweive.db')
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    __tablename__ = 'USERS'
    __table_args__ = {'extend_existing':True}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    user_type = db.Column(db.String(10), nullable = False)
    phone_number = db.Column(db.String(100))
    cc_number = db.Column(db.String(100))
    email = db.Column(db.String(50), nullable = False, unique = True)
    def get_id(self):
        return self.id

class OUApp(db.Model):
    __tablename__ = 'OUAPPLICATIONS'
    __table_args__ = {'extend_existing':True}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)
    user_type = db.Column(db.String(10), nullable = False)
    phone_number = db.Column(db.String(100))
    email = db.Column(db.String(50), nullable = False, unique = True)
    def get_id(self):
        return self.id

class Process_Items(db.Model, UserMixin):
    __tablename__='PROCESS_ITEMS'
    id=db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    key_words = db.Column(db.Text, nullable=False )
    seller_id = db.Column(db.Integer,ForeignKey("USERS.id"))
    time_limit = db.Column(DateTime(timezone=True), server_default=func.now())

class Items(db.Model, UserMixin):
    __tablename__='ITEMS'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    key_words = db.Column(db.Text, nullable=False )
    seller_id = db.Column(db.Integer,ForeignKey("USERS.id"))
    time_limit = db.Column(DateTime(timezone=True), server_default=func.now())
    highest_bid = db.Column(db.Integer, nullable=False)

 
class Transactions(db.Model, UserMixin):
    __tablename__= 'TRANSACTIONS'
    id = db.Column(db.Integer, primary_key = True)
    date_and_time = db.Column(DateTime(timezone=True), server_default=func.now())
    item_id = db.Column(db.Integer,ForeignKey("ITEMS.id"), nullable=False)
    buyer_id = db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False, unique=True)
    seller_id = db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False, unique=True)
    highest_bid = db.Column(db.Integer, nullable=False)

class Bids(db.Model, UserMixin):
    __tablename__= 'BIDS'
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)
    highest_bid = db.Column(db.Integer, nullable=False)
    bidder_id = db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    time_stamp = db.Column(DateTime(timezone=True), server_default=func.now())

class Rate(enum.Enum):
    one = 1 
    two = 2
    three = 3
    four = 4
    five = 5 


class Give_Rating(db.Model, UserMixin):
    __tablename__= 'RATINGS'
    id= db.Column(db.Integer, primary_key=True)
    trans_id=db.Column(db.Integer, ForeignKey("TRANSACTIONS.id"), nullable=False)
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    item_id = db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)
    rating = db.Column(Enum(Rate), nullable=False)
    

class Complaints(db.Model, UserMixin):
    __tablename__='COMPLAINTS'
    id= db.Column(db.Integer, primary_key = True)
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    complaint_cnt=db.Column(db.Integer, nullable=False)
    reason=db.Column(db.Text, nullable=False)

class Sus_Reports(db.Model, UserMixin):
    __tablename__='SUS_REPORTS'
    id=db.Column(db.Integer, primary_key=True)
    item_id=db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)

class Sus_Items(db.Model, UserMixin):
    __tablename__='SUS_ITEMS'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    item_id=db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)

class Police_Reports(db.Model, UserMixin):
    __tablename__='POLICE_REPORTS'
    id=db.Column(db.Integer, primary_key=True)
    date_and_time=db.Column(DateTime(timezone=True), server_default=func.now())
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    report_id=db.Column(db.Integer, ForeignKey("SUS_REPORTS.id"), nullable=False)
    item_id=db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)

class Users_Items_Blocklist(db.Model, UserMixin):
    __tablename__='USERS_ITEMS_BLOCKLIST'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    item_id= db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)

class Users_Blacklist(db.Model, UserMixin):
    __tablename__='USERS_BLACKLIST'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
 
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(min = 8, max = 80)])
    phone = StringField('Phone Number', validators=[InputRequired(), Length(min=9, max = 20)])

app.app_context().push()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# use python -m flask to run the app in VSCode
@app.route("/", methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@app.route('/OUApplication', methods = ['GET', 'POST'])
def OUApplication():
    form = RegisterForm()

    if form.validate_on_submit():
        # new_user = User(username=form.username.data, email = form.email.data, phone_number = form.phone.data, password = form.password.data, user_type = "OU")
        # db.session.add(new_user)
        new_app = OUApp(username=form.username.data, email = form.email.data, phone_number = form.phone.data, password = form.password.data, user_type = "OU")
        db.session.add(new_app)
        db.session.commit()
        return '<h1>new user created</h1>'
    return render_template("OUApplication.html", form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('home'))
        return '<h1>invalid username or password</h1>'
    return render_template('login.html', form = form)

# @app.route("/welcome") 
# @login_required
# def welcome():
#     return render_template(
#         "welcome.html",
#         name=current_user.username,
#         date=datetime.now()
#     )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/item", methods = ['GET','POST'])
def itemPage():
    item = db.session.query(Items).first() # just using the first item for updating the db
    # if the highest bid ends in two 0s, we have to format it with '.2f'
    # select highest_bid from Items where id=1
    highest_bid = item.highest_bid
    return render_template(
        "Siemaitem.html",
        image_address="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title=item.title,
        seller_id=item.id,
        time_left="December 14, 2022",
        highest_bid=highest_bid,
        highest_bid_constraint=highest_bid+1,
        item_description="Van Gogh’s paintings of Sunflowers are among his most famous. He did them in Arles, in the south of France, in 1888 and 1889. Vincent painted a total of five large canvases with sunflowers in a vase, with three shades of yellow ‘and nothing else’. In this way, he demonstrated that it was possible to create an image with numerous variations of a single colour, without any loss of eloquence.")

@app.route("/item/place-bid", methods = ['GET','POST'])
def placeBid():
    curDate = datetime.now()
    item = db.session.query(Items).first() # just using the first item for updating the db
    if request.method == "POST":
       # getting input with user = fUser in HTML form
        highest_bid = item.highest_bid
        bid = int(request.form.get("fBid"))
        db.session.query(Items).filter(Items.id == 1).update({'highest_bid': bid})
        newBid = Bids(item_id = item.id, highest_bid = bid, bidder_id=current_user.id, time_stamp=curDate)
        db.session.add(newBid)   
        db.session.commit()
        highest_bid = item.highest_bid # for frontend, have to update the actual item and add to bids table
    allBids = Bids.query.filter(Bids.item_id==item.id).order_by(Bids.highest_bid.desc()).all()
    return render_template(
        "Siemaitem.html",
        image_address="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title=item.title,
        seller_id=item.seller_id,
        time_left=(item.time_limit - curDate).days,
        deadline = item.time_limit.date(),
        highest_bid=highest_bid,
        highest_bid_constraint=highest_bid+1,
        item_description="Van Gogh’s paintings of Sunflowers are among his most famous. He did them in Arles, in the south of France, in 1888 and 1889. Vincent painted a total of five large canvases with sunflowers in a vase, with three shades of yellow ‘and nothing else’. In this way, he demonstrated that it was possible to create an image with numerous variations of a single colour, without any loss of eloquence.",
        allBids=allBids)


@app.route("/report-item", methods = ['GET', 'POST'])
def sendReport():
    item = db.session.query(Items).first()
    newReport = Sus_Reports(item_id = item.id)
    db.session.add(newReport)   
    db.session.commit()
    return render_template(
        "reportPage.html",
        itemName = item.title
    )

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def accountPage():
    return render_template(
        "accountPage.html",
        name=current_user.username,
    )

@app.route("/account/collect-transaction-history", methods = ['GET', 'POST'])
@login_required
def collectTransactions():
    # this is for SUs only
    return render_template(
        "accountPage.html",
        transactions = Transactions.query.all(),
        name=current_user.username
    )

@app.route("/account/collect-transaction-history/user", methods = ['GET', 'POST'])
@login_required
def collectTransactionsUser():
    # this is for SUs only
    if request.method == "POST":
       # getting input with user = fUser in HTML form
        user = request.form.get("fUser")
        timefield = request.form.get("fTime")
        curDate = datetime.now()
        if ((timefield != '') & (user != '')): # if both are filled
            timePeriod = int(timefield) + 1 
            queryDate = curDate - timedelta(days=timePeriod) 
            transactions = Transactions.query.filter(((Transactions.seller_id==user) | (Transactions.buyer_id==user)) & (Transactions.date_and_time >= queryDate))
        elif(timefield == ''):
            transactions = Transactions.query.filter((Transactions.seller_id==user) | (Transactions.buyer_id==user))
        elif(user == ''):
            timePeriod = int(timefield) + 1 # user includes days
            # current date: 2022-12-12 23:47:36.185863
            queryDate = curDate - timedelta(days=timePeriod) 
            transactions = Transactions.query.filter((Transactions.date_and_time >= queryDate))
        return render_template(
            "accountPage.html",
            transactions = transactions,
            name=current_user.username,
            maxNumDays = curDate - datetime.min - timedelta(days=2)
        )

@app.route("/account/transactions-history", methods = ['GET', 'POST'])
@login_required
def transactionsHistory():
    # this is for OUs only
    transactions = Transactions.query.filter((Transactions.seller_id==current_user.id) | (Transactions.buyer_id==current_user.id))
    return render_template(
        "accountPage.html",
        transactions = transactions,
        name=current_user.username
    )


@app.route("/search", methods = ['GET', 'POST'])
def searchPage():
    return render_template(
        "search.html",
        image="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title="Vincent Van Gogh Replica Painting Sunflowers",
        highest_bid=db.session.query(Items).first().highest_bid
    )
