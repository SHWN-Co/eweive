from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import or_
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruhmoment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'eweivenew.db')
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from forms import LoginForm, RegisterForm, buildUpdateInfo, submitItemForm, complaintsForm, rateForm, updatePasswordForm, addCCForm, withdrawForm, depositForm, postForm, searchForm, postForm1, postForm2, postForm3
from models import User, OUApp, Process_Items, Items, Transactions, Bids, Give_Rating, Complaints, Sus_Reports, Sus_Items, Police_Reports, Users_Items_Blocklist, Users_Blacklist
from setup import returnBalance, db_run

app.app_context().push()
db_run()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
# use python -m flask to run the app in VSCode
@app.route("/", methods=['GET','POST'])
def home():
    return render_template("homepage.html")

@app.route("/allItems")
def browse():
    items = Items.query.all()
    return render_template('browse.html', results=items)

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
            starting_bid=float(form.starting_bid.data)*100
            new_item = Process_Items(title=form.title.data, image = form.image.data, key_words = form.key_words.data, seller_id=current_user.id, time_limit = form.time_limit.data, description=form.description.data, starting_bid=starting_bid)
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
       #flash('new complaint submitted, awaiting settlement') 
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
                user = Items(title = user.title, image = user.image,key_words=user.key_words, seller_id=user.seller_id, time_limit=user.time_limit, highest_bid=int(round(float(user.starting_bid)/100)), description=user.description)
                db.session.add(user)
                Process_Items.query.filter_by(id=id).delete()
                db.session.commit()
            
            return redirect(url_for('showItems'))
    return render_template('finalizeItem.html', id = id, title = user.title, image = user.image,key_words=user.key_words, seller_id=user.seller_id, time_limit=user.time_limit, status=user.status,description=user.description,starting_bid = user.starting_bid, form = form)

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/item/<id>", methods = ['GET','POST'])
def itemPage(id=0):
    display_item = Items.query.filter_by(id=id).first()
    if (id == 0 or not display_item): return 'item not found!'
    allBids = Bids.query.filter(Bids.item_id==display_item.id).order_by(Bids.highest_bid.desc()).all()
    return render_template(
        "item.html",
        item_id=display_item.id,
        allBids=allBids,
        image_address=display_item.image,
        item_title=display_item.title,
        seller_id=display_item.seller_id,
        end_date=display_item.time_limit,
        highest_bid=display_item.highest_bid,
        highest_bid_constraint=display_item.highest_bid+1,
        item_description=display_item.description)

@app.route("/item/<id>/place-bid", methods = ['GET','POST'])
def placeBid(id=0):
    curDate = datetime.now()
    item = Items.query.filter_by(id=id).first() # just using the first item for updating the db
    if item.seller_id == current_user.id:
        flash('cant bid on your own item!')
        return redirect(url_for('itemPage', id = item.id))
    if request.method == "POST":
        checkSold = Transactions.query.filter_by(item_id=item.id).first()
        if checkSold:
            flash('item has been sold!')
            return redirect(url_for('itemPage', id = item.id))
       # getting input with user = fUser in HTML form
        highest_bid = item.highest_bid
        bid = int(request.form.get("fBid"))
        if (bid > current_user.balance/100):
            flash('you do not have enough money in your account!')
            return redirect(url_for('itemPage', id = item.id))
        checkBidder = Bids.query.filter(Bids.bidder_id== current_user.id, Bids.item_id == item.id).first()
        if checkBidder:
            checkBidder.highest_bid = bid
        else:
            newBid = Bids(item_id = item.id, highest_bid = bid, bidder_id=current_user.id, time_stamp=curDate)
            db.session.add(newBid)  
        db.session.query(Items).filter(Items.id == id).update({'highest_bid': bid})
        db.session.commit()
    allBids = Bids.query.filter(Bids.item_id==item.id).order_by(Bids.highest_bid.desc()).all()
    return render_template(
        "item.html",
        item_id=item.id,
        image_address=item.image,
        item_title=item.title,
        seller_id=item.seller_id,
        time_left=(item.time_limit - curDate).days,
        deadline = item.time_limit.date(),
        highest_bid=item.highest_bid,
        highest_bid_constraint=item.highest_bid+1,
        item_description=item.description,
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
    if current_user.cc_number is None:
        return redirect(url_for('updateCard'))
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
    if current_user.cc_number is None:
        return redirect(url_for('updateCard'))
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


@app.route("/account/collect-transaction-history", methods = ['GET', 'POST'])
@login_required
def collectTransactions():
    # this is for SUs only
    return render_template(
        "collectTransactionsHistory.html",
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
            "collectTransactionsHistory.html",
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
        "collectTransactionsHistory.html",
        transactions = transactions,
        name=current_user.username
    )


@app.route("/search", methods = ['GET', 'POST'])
def searchPage():
    # form = searchForm()
    # if form.validate_on_submit():
    #     input = form.search.data
    #     query = f'%{input}'
    #     filter_list = [Items.title.ilike(query), Items.key_words.ilike(query)]
    #     results = Items.query.filter(or_(*filter_list))
    results = Items.query.filter(Items.id==0)
    if request.method == "POST": 
        input = request.form.get("input")
        query = f'%{input}%'
        filter_list = [Items.title.ilike(query), Items.key_words.ilike(query)]
        results = Items.query.filter(or_(*filter_list))
    return render_template(
        "search.html",
        image="https://iiif.micr.io/TZCqF/full/1280,/0/default.jpg",
        item_title="Vincent Van Gogh Replica Painting Sunflowers",
        results = results
    )

@app.route("/account/validate-reports", methods = ['GET', 'POST'])
@login_required
def validateReports():
    # this is for SUs only
    return render_template(
        "validateReports.html",
        transactions = Transactions.query.all(),
        name=current_user.username,
        reportedItems = Sus_Reports.query.all()
    )

# needs fixing
@app.route("/account/validate-reports/confirm", methods = ['GET', 'POST'])
@login_required
def confirmReport():
    # this is for SUs only
    if request.method == "POST":
        # getting input with user = fUser in HTML form
        itemReported = request.form.get("fitemId") # id of what you want to delete from items
        # using item id, find the seller
        sellersid = Items.query.filter(Items.id==itemReported).first().seller_id
        usertoBList = Users_Items_Blocklist(seller_id=sellersid, item_id=itemReported) # add the user to items blocklist
        db.session.add(usertoBList)
        Sus_Reports.query.filter_by(item_id=itemReported).delete() # delete from sus reports
        User.query.filter_by(id=sellersid).delete() # delete from users
        Items.query.filter_by(seller_id=sellersid).delete() # delete from users
        db.session.commit()
        return render_template(
            "validateReports.html",
            transactions = Transactions.query.all(),
            name=current_user.username,
            reportedItems = Sus_Reports.query.all()
        )

@app.route("/itemsOnSale", methods = ['GET', 'POST'])
@login_required
def displayItemsOnSale():
    id = current_user.id 
    items = Items.query.filter_by(seller_id = id)
    items_headers = Items.__table__.columns.keys()
    now = datetime.now()
    curr_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return render_template('itemsOnSale.html', items = items, headers = items_headers)

@app.route("/sellItemPage/<id>", methods = ['GET', 'POST'])
@login_required
def sellItemPage(id=0):
    item = Items.query.filter_by(id=id).first()
    if (id == 0 or not item): return redirect(url_for('displayItemsOnSale'))
    allBids = Bids.query.filter(Bids.item_id==item.id).order_by(Bids.highest_bid.desc()).all()
    if request.method == 'POST':
        checkSold = Transactions.query.filter_by(item_id=item.id).first()
        if checkSold:
            flash('item has been sold!')
            return redirect(url_for('sellItemPage', id = item.id))
        now = datetime.now()
        bidder_id = request.form['bidder']
        seller = User.query.filter_by(id=current_user.id).first()
        bidder = User.query.filter_by(id=bidder_id).first()
        getBid = Bids.query.filter(Bids.bidder_id==bidder_id, Bids.item_id==item.id).first()
        if seller and bidder and getBid and bidder.balance >= getBid.highest_bid:
            bidder.balance = bidder.balance - (getBid.highest_bid*100)
            seller.balance = seller.balance + (getBid.highest_bid*100)
            new_transaction = Transactions(item_id=item.id, buyer_id=bidder_id, seller_id=current_user.id,highest_bid=getBid.highest_bid)
            db.session.add(new_transaction)
            db.session.commit()
        else:
            flash('The user does not have enough funds on their account.')
            return redirect(url_for('sellItemPage', id = item.id))
        return redirect(url_for('displayItemsOnSale'))
    return render_template('sellItem.html', item = item, allBids = allBids)