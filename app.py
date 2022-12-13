import enum
from flask import Flask, render_template, request, url_for, redirect, session, flash
from sqlalchemy import DateTime, Enum, ForeignKey, func, Integer # (once we start creating html pages)
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, BooleanField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime

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
    status = db.Column(db.Text, nullable = False, default= "Pending")
    description = db.Column(db.Text, nullable=False)

class Items(db.Model, UserMixin):
    __tablename__='ITEMS'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    key_words = db.Column(db.Text, nullable=False )
    seller_id = db.Column(db.Integer,ForeignKey("USERS.id"))
    time_limit = db.Column(DateTime(timezone=True), server_default=func.now())
    highest_bid = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

 
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

# class Rate(enum.Enum):
#     one = 1 
#     two = 2
#     three = 3
#     four = 4
#     five = 5 


class Give_Rating(db.Model, UserMixin):
    __tablename__= 'RATINGS'
    id= db.Column(db.Integer, primary_key=True)
    trans_id=db.Column(db.Integer, ForeignKey("TRANSACTIONS.id"), nullable=False)
    user_id=db.Column(db.Integer, ForeignKey("USERS.id"), nullable=False)
    item_id = db.Column(db.Integer, ForeignKey("ITEMS.id"), nullable=False)
    #rating = db.Column(Enum(Rate), nullable=False)
    rating= db.Column(db.Integer, nullable=False)
    

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
    email = db.Column(db.String(50), ForeignKey("USERS.email"), nullable=False)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
 
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(min = 8, max = 80)])
    phone = StringField('Phone Number', validators=[InputRequired(), Length(min=9, max = 20)])

class submitItemForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=20)])
    image = StringField('Image Address', validators=[InputRequired(), Length(min=6, max=80)])
    key_words = StringField('Key Words', validators=[InputRequired(), Length(min=2, max=80)])
    time_limit = DateTimeField('Time Limit', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired(), Length(min=2, max=80)])
 
class complaintsForm(FlaskForm):
    reason = StringField('Reasoning', validators=[InputRequired(), Length(min=4, max=300)])
    
 
class rateForm(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Rate', choices =[('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5)], validators=[InputRequired()])

    
class postForm1(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Settle?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])


class postForm2(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Approve?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])

class postForm3(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Remove?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])


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



# @app.route('/showItems')
# def showItems():
#    return render_template('showItems.html', Process_Items = Process_Items.query.all() )


@app.route('/OUcomplaint')
def OUcomplaint():
   return render_template('OUcomplaint.html', Complaints = Complaints.query.all() )

@app.route('/OUitems')
def OUitems():
   return render_template('OUitems.html', Process_Items = Process_Items.query.all() )




@app.route("/submitItem", methods = ['GET', 'POST'])
def submitItem():
    form = submitItemForm()

    if form.validate_on_submit():
        # new_user = User(username=form.username.data, email = form.email.data, phone_number = form.phone.data, password = form.password.data, user_type = "OU")
        # db.session.add(new_user)
            new_item = Process_Items(title=form.title.data, image = form.image.data, key_words = form.key_words.data, seller_id=current_user.id, time_limit = form.time_limit.data, description=form.description.data)
            # seller_id= current_user.id
            db.session.add(new_item)
            db.session.commit()
            flash('new item submitted, awaiting processing') 
            return redirect(url_for('showItems'))
    return render_template("submitItem.html", form = form)




@app.route("/finalizeItem", methods = ['GET', 'POST'])
@login_required
def showItems():
    if current_user.user_type == 'OU':
       #return Complaints.query.filter_by(id=current_user.id)
       flash('new complaint submitted, awaiting settlement') 
       return redirect(url_for('home'))
    pending = Process_Items.query.all()
    pending_headers = Process_Items.__table__.columns.keys()
    if request.method == 'POST':
        user_id = request.form['item_container']
        return redirect(url_for('finalizeItem', id = user_id))
    return render_template('showItems.html', pending = pending, headers = pending_headers)

@app.route("/finalizeItem/<id>", methods = ['GET', 'POST'])
@login_required
def finalizeItem(id=0):
    user = Process_Items.query.filter_by(id=id).first()
    form = postForm2()
    if form.validate_on_submit():
        if user:
            if (form.choice.data == 'Yes'):
                user = Items(title = user.title, image = user.image,key_words=user.key_words, seller_id=user.seller_id, time_limit=user.time_limit, highest_bid=0, description=user.description)
                db.session.add(user)
                Process_Items.query.filter_by(id=id).delete()
                db.session.commit()
            
            return redirect(url_for('showItems'))
    return render_template('finalizeItem.html', id = id, title = user.title, image = user.image,key_words=user.key_words, seller_id=user.seller_id, time_limit=user.time_limit, status=user.status,description=user.description, form = form)



@app.route("/finalizeUser", methods = ['GET', 'POST'])
@login_required
def showUsers():
    if current_user.user_type == 'OU':
       return redirect(url_for('home'))
    pending = User.query.all()
    pending_headers = User.__table__.columns.keys()
    if request.method == 'POST':
        user_id = request.form['item_container']
        return redirect(url_for('finalizeUser', id = user_id))
    return render_template('showUsers.html', pending = pending, headers = pending_headers)

@app.route("/finalizeUser/<id>", methods = ['GET', 'POST'])
@login_required
def finalizeUser(id=0):
    user = User.query.filter_by(id=id).first()
    form = postForm3()
    if form.validate_on_submit():
        if user:
            if (form.choice.data == 'Yes'):
                user = Users_Blacklist(user_id=user.id, email=user.email)
                db.session.add(user)
                User.query.filter_by(id=id).delete()
                db.session.commit()
            
            return redirect(url_for('showUsers'))
    return render_template('finalizeUser.html', id = id, username = user.username, user_type = user.user_type,phone_number=user.phone_number,cc_number=user.cc_number, email=user.email, form = form)





@app.route("/finalizeComplaint", methods = ['GET', 'POST'])
@login_required
def showComplaints():
    if current_user.user_type == 'OU':
       #return Complaints.query.filter_by(id=current_user.id)
       flash('new complaint submitted, awaiting settlement') 
       return redirect(url_for('home'))
    pending = Complaints.query.all()
    pending_headers = Complaints.__table__.columns.keys()
    if request.method == 'POST':
        user_id = request.form['item_container']
        return redirect(url_for('finalizeComplaint', id = user_id))
    return render_template('showComplaints.html', pending = pending, headers = pending_headers)

@app.route("/finalizeComplaint/<id>", methods = ['GET', 'POST'])
@login_required
def finalizeComplaint(id=0):
    user = Complaints.query.filter_by(id=id).first()
    form = postForm1()
    if form.validate_on_submit():
        if user:
            if (form.choice.data == 'Yes'):
                Complaints.query.filter_by(id=id).delete()
                db.session.commit()
            
            return redirect(url_for('showComplaints'))
    return render_template('finalizeComplaint.html', id = id, user_id = user.user_id, complaint_cnt=user.complaint_cnt, reason = user.reason, form = form)


# @app.route('/showComplaints')
# def showComplaints():
#      return render_template('showComplaints.html', Complaints = Complaints.query.all() )


@app.route("/fileComplaint", methods = ['GET', 'POST'])
def fileComplaint():
    form = complaintsForm()

    if form.validate_on_submit():
        
        #db.session.query(Complaints).filter(new_complaint.user_id==current_user.id).count()
        new_complaint = Complaints(user_id=current_user.id, complaint_cnt=db.session.query(Complaints).filter(Complaints.user_id==current_user.id).count(), reason=form.reason.data)
# # complaint_cnt=1
        db.session.add(new_complaint)
        db.session.commit()
        flash('Complaint submitted, awaiting settlement decision') 
        return redirect(url_for('showComplaints'))
    return render_template("fileComplaint.html", form = form)



 
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
    return render_template(
        "item.html",
        image_address="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title="Vincent Van Gogh Replica Painting Sunflowers",
        seller_id="342",
        end_date="December 14, 2022",
        highest_bid="$100.00",
        highest_bid_constraint="$101.00",
        item_description="Van Gogh’s paintings of Sunflowers are among his most famous. He did them in Arles, in the south of France, in 1888 and 1889. Vincent painted a total of five large canvases with sunflowers in a vase, with three shades of yellow ‘and nothing else’. In this way, he demonstrated that it was possible to create an image with numerous variations of a single colour, without any loss of eloquence.")

@app.route("/report-item", methods = ['GET', 'POST'])
def reportPage():
    return render_template(
        "reportPage.html"
    )

@app.route("/ratePage", methods = ['GET', 'POST'])
def ratePage():
    form = rateForm()
    item = db.session.query(Items).first()
    if form.validate_on_submit() :
            if (form.choice.data == 'one'):
                #db.session.query(Give_Rating).filter(Give_Rating.trans_id)
                #new_rate= Give_Rating(trans_id=Give_Rating.trans_id, user_id=current_user.id, item_id=Give_Rating.item_id,rating=1)
                
                new_rate= Give_Rating(trans_id=item.id, user_id=current_user.id, item_id=item.seller_id,rating=1)
                #new_rate= Give_Rating(trans_id=db.session.query(Give_Rating).filter(Give_Rating.trans_id), user_id=current_user.id, item_id=Give_Rating.item_id,rating=1)
                db.session.add(new_rate)
                db.session.commit()
                
            elif (form.choice.data == 'two'):
                new_rate= Give_Rating(trans_id=item.id, user_id=current_user.id, item_id=item.seller_id,rating=2)
                db.session.add(new_rate)
                db.session.commit()
                
            elif (form.choice.data == 'three'):
                new_rate= Give_Rating(trans_id=item.id, user_id=current_user.id, item_id=item.seller_id,rating=3)
                db.session.add(new_rate)
                db.session.commit()
                
            elif (form.choice.data == 'four'):
                new_rate= Give_Rating(trans_id=item.id, user_id=current_user.id, item_id=item.seller_id,rating=4)
                db.session.add(new_rate)
                db.session.commit()
                
            elif (form.choice.data == 'five'):
                new_rate= Give_Rating(trans_id=item.id, user_id=current_user.id, item_id=item.seller_id,rating=5)
                db.session.add(new_rate)
                db.session.commit()
                
            return redirect(url_for('home'))
    return render_template("ratePage.html", form=form)

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def accountPage():
    return render_template(
        "accountPage.html",
        name=current_user.username,
    )

@app.route("/search", methods = ['GET', 'POST'])
def searchPage():
    return render_template(
        "search.html",
        image="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title="Vincent Van Gogh Replica Painting Sunflowers",
        highest_bid="$100.00"
    )


