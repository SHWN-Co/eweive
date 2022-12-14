from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, TextAreaField, RadioField, SearchField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, Regexp

currencyInputRegex = r"^[0-9]+\.[0-9]{2}$"
numberRegex = r"^[0-9]+$"

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
    return updateInfo()

class submitItemForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=100)])
    image = StringField('Image Address', validators=[InputRequired(), Length(min=6, max=180)])
    key_words = StringField('Key Words', validators=[InputRequired(), Length(min=2, max=180)])
    time_limit = DateTimeField('Time Limit', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired(), Length(min=2, max=500)])
    starting_bid = StringField('Starting Bid', validators=[InputRequired(), Regexp(regex = currencyInputRegex, message="Notice: Valid Input Dollar Amount: x.xx")])
 
class complaintsForm(FlaskForm):
    reason = StringField('Reasoning', validators=[InputRequired(), Length(min=4, max=300)])
    
 
class rateForm(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Rate', choices =[('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5)], validators=[InputRequired()])


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

class postForm1(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Settle?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])

class postForm2(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Approve?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])

class postForm3(FlaskForm):
    body = TextAreaField('Message', default ="", validators=[Length(min=0, max=500)])
    choice = RadioField('Remove?', choices =[('Yes', 'Yes'), ('No', 'No')], default = 'No', validators=[InputRequired()])