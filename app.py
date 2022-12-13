import enum
from flask import Flask, render_template, request, url_for, redirect, session, flash
from sqlalchemy import DateTime, Enum, ForeignKey, func, Integer, or_
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SearchField
from wtforms.validators import InputRequired, Email, Length, Regexp
from datetime import datetime

currencyInputRegex = r"^[0-9]+\.[0-9]{2}$"
numberRegex = r"^[0-9]+$"

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
    balance = db.Column(db.Integer, nullable = False)
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
    description = db.Column(db.Text, nullable = False)

class Items(db.Model, UserMixin):
    __tablename__='ITEMS'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    key_words = db.Column(db.Text, nullable=False )
    seller_id = db.Column(db.Integer,ForeignKey("USERS.id"))
    time_limit = db.Column(DateTime(timezone=True), server_default=func.now())
    highest_bid = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable = False)

 
class Transactions(db.Model, UserMixin):
    __tablename__= 'TRANSACTIONS'
    id = db.Column(db.Integer, primary_key = True)
    date_and_time = db.Column(DateTime(timezone=True), server_default=func.now())
    item_id = db.Column(db.Integer,ForeignKey("ITEMS.id"), nullable=False)
    buyer_id = db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False, unique=True)
    seller_id = db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False, unique=True)
    highest_bid = db.Column(db.Integer, nullable=False)

class Bid(db.Model, UserMixin):
    __tablename__= 'BID'
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)
    highest_bid = db.Column(db.Integer, nullable=False)

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
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"), Length(min = 1, max = 80)])
    phone = StringField('Phone Number', validators=[InputRequired(), Regexp(regex = numberRegex, message = "Notice: Only input numbers" ), Length(min=9, max = 20)])

def buildUpdateInfo(curr_user="", curr_email="", curr_phone=""):
    class updateInfo(FlaskForm):
        username = StringField('Username', default = curr_user, validators=[InputRequired(), Length(min=4, max=20)])
        email = StringField('Email', default = curr_email, validators=[InputRequired(), Email(message="Invalid email"), Length(min=1, max = 80)])
        phone = StringField('Phone Number', default = curr_phone, validators=[InputRequired(), Regexp(regex = numberRegex, message = "Notice: Only input numbers" ), Length(min=9, max = 20)])
    return updateInfo();

class updatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired(), Length(min=6, max=80)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm_password = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=6, max=80)])

class addCCForm(FlaskForm):
    cc_number = StringField('Credit Card Number', validators=[InputRequired(), Regexp(regex = numberRegex, message = "Notice: Only input numbers" ), Length(min = 12, max =80)])

class withdrawForm(FlaskForm):
    withdraw = StringField('Withdraw Amount', validators=[InputRequired(), Regexp(regex = currencyInputRegex, message="Notice: Valid Input Dollar Amount: x.xx")])

class depositForm(FlaskForm):
    deposit = StringField('Deposit Amount', validators=[InputRequired(), Regexp(regex = currencyInputRegex, message="Notice: Valid Input Dollar Amount: x.xx")])

class postForm(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Approve?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])

class searchForm(FlaskForm):
    search = SearchField('', validators=[InputRequired(), Length(min=1, max=500)])

#function to return balance
def returnBalance(balance):
    a = 0
    if balance is not None:
        a = balance/100
    return a

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
        new_app = OUApp(username=form.username.data, email = form.email.data, phone_number = form.phone.data, password = form.password.data, user_type = "OU")
        db.session.add(new_app)
        db.session.commit()
        flash('Application successfully submitted')
        return redirect(url_for('home'))
    return render_template("OUApplication.html", form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and (user.password == form.password.data):
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
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

@app.route("/item/<id>", methods = ['GET','POST'])
def itemPage(id=0):
    display_item = Items.query.filter_by(id=id).first()
    if (id == 0 or not display_item): return 'item not found!'
    return render_template(
        "item.html",
        image_address=display_item.image,
        item_title=display_item.title,
        seller_id=display_item.seller_id,
        end_date=display_item.time_limit,
        highest_bid=f'${display_item.highest_bid}',
        highest_bid_constraint=f'${display_item.highest_bid+1}',
        item_description=display_item.description)

@app.route("/report-item", methods = ['GET', 'POST'])
def reportPage():
    return render_template(
        "reportPage.html"
    )

@app.route("/account")
@login_required
def accountPage():
    user_balance = returnBalance(current_user.balance)
    return render_template(
        "accountPage.html",
        name=current_user.username,
        balance = '%.2f' % user_balance
    )

@app.route("/change_info", methods = ['GET', 'POST'])
@login_required
def changeInfo():
    form = buildUpdateInfo(current_user.username, current_user.email, current_user.phone_number)
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        if user:
            user.username = form.username.data
            user.email = form.email.data
            user.phone_number = form.phone.data
            db.session.commit()
            flash('successfully changed user info')
            return redirect(url_for('accountPage'))
    return render_template("changeInfo.html", form = form)

@app.route("/change_pass", methods = ['GET', 'POST'])
@login_required
def changePass():
    updatePass = updatePasswordForm()
    user = User.query.filter_by(id=current_user.id).first()
    if updatePass.validate_on_submit():
        if user:
            if (user.password == updatePass.current_password.data and updatePass.new_password.data == updatePass.confirm_password.data):
                user.password = updatePass.new_password.data
                db.session.commit()
                flash('successfully changed password')
                return redirect(url_for('accountPage'))
            else:
                flash('Current password does not match OR new password and confirm new password do not match')
    return render_template("changePass.html", updatePass = updatePass)

@app.route("/cardUpdate", methods = ['GET', 'POST'])
@login_required
def updateCard():
    form = addCCForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        if user:
            user.cc_number = form.cc_number.data
            db.session.commit()
            flash('successfully updated card')
            return redirect(url_for('accountPage'))
    return render_template("updateCard.html", form = form)

@app.route("/withdraw", methods = ['GET', 'POST'])
@login_required
def withdraw():
    form = withdrawForm()
    user = User.query.filter_by(id=current_user.id).first()
    user_balance = returnBalance(current_user.balance)
    if form.validate_on_submit():
        input = float(form.withdraw.data)
        if user:
            if user.balance is None:
                user.balance = 0
                db.session.commit()
            if input < 0.01:
                flash('Invalid withdrawal amount!')
            elif input > user_balance:
                flash('Attempting to withdraw more than your account balance!')
            else:
                user.balance = user.balance - (input*100)
                db.session.commit()
                flash('Withdrew $%s from your account balance.' % form.withdraw.data)
                return redirect(url_for('accountPage'))
    return render_template('withdraw.html', form = form, balance = '%.2f' % user_balance)

@app.route("/deposit", methods = ['GET', 'POST'])
@login_required
def deposit():
    form = depositForm()
    user = User.query.filter_by(id=current_user.id).first()
    user_balance = returnBalance(current_user.balance)
    if form.validate_on_submit():
        input = float(form.deposit.data)
        if user:
            if user.balance is None:
                user.balance = 0
                db.session.commit()
            if input > 0.01:
                user.balance = user.balance + (input*100)
                db.session.commit()
                flash('Deposited $%s to your account balance' % form.deposit.data)
                return redirect(url_for('accountPage'))
            else:
                flash('Invalid deposit amount!')
    return render_template('deposit.html', form = form, balance = '%.2f' % user_balance)

@app.route("/reviewApplications", methods = ['GET', 'POST'])
@login_required
def approveApps():
    if current_user.user_type == 'OU':
        return redirect(url_for('home'))
    pending = OUApp.query.all()
    pending_headers = OUApp.__table__.columns.keys()
    if request.method == 'POST':
        user_id = request.form['item_container']
        return redirect(url_for('approve_user', id = user_id))
    return render_template('approveApps.html', pending = pending, headers = pending_headers)

@app.route("/reviewApplications/<id>", methods = ['GET', 'POST'])
@login_required
def approve_user(id=0):
    user = OUApp.query.filter_by(id=id).first()
    if (id == 0 or not user): 
        return redirect(url_for('approveApps'))
    form = postForm()
    if form.validate_on_submit():
        if user:
            if (form.choice.data == 'Yes'):
                new_user = User(username=user.username, email = user.email, phone_number = user.phone_number, password = user.password, user_type = "OU", balance = 0)
                db.session.add(new_user)
            OUApp.query.filter_by(id=id).delete()
            db.session.commit()
            return redirect(url_for('approveApps'))
    return render_template('approveUser.html', id = id, name = user.username, phone = user.phone_number, email = user.email, form = form)


@app.route("/search", methods = ['GET', 'POST'])
def searchPage():
    # form = searchForm()
    # if form.validate_on_submit():
    #     input = form.search.data
    #     query = f'%{input}'
    #     filter_list = [Items.title.ilike(query), Items.key_words.ilike(query)]
    #     results = Items.query.filter(or_(*filter_list))
    results = []
    if request.method == "POST": 
        input = request.form.get("input")
        query = f'%{input}%'
        filter_list = [Items.title.ilike(query), Items.key_words.ilike(query)]
        results = Items.query.filter(or_(*filter_list))
    return render_template(
        "search.html",
        image="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title="Vincent Van Gogh Replica Painting Sunflowers",
        highest_bid="$100.00",
        results = results
    )