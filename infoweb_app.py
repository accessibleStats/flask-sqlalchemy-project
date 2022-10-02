"""

Web Application Framework - user management with SQLite3 database

"""
from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from aux import dburi, csrftoken
from datetime import datetime


# instantiate the application
app = Flask(__name__)
# generate secret key to prevent CSRF attacks
app.secret_key = csrftoken
# specify database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = dburi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# declare database object
sqldb = SQLAlchemy(app)


# Website Patrons table
class Patrons(sqldb.Model):
    __tablename__ = 'users'

    id = sqldb.Column(sqldb.Integer, primary_key=True)
    username = sqldb.Column(sqldb.String(100), nullable=False)
    email = sqldb.Column(sqldb.String(80), unique=True, nullable=False)
    passworda = sqldb.Column(sqldb.String(100), nullable=False)
    passwordb = sqldb.Column(sqldb.String(100), nullable=False)
    password = sqldb.Column(sqldb.String(100), nullable=False)
    date = sqldb.Column(sqldb.DateTime(timezone=True),
                        server_default=func.now())

    def __init__(self, username, email, passworda, passwordb, password, date):
        self.username = username
        self.email = email
        self.passworda = passworda
        self.passwordb = passwordb
        self.password = password
        self.date = date

    def __repr__(self):
        return f'<{self.username} - {self.id}>'


# signup FlaskForm
class SignupForm(FlaskForm):
    inputusername = StringField("Enter your Username", validators=[
                                DataRequired()], id='usernamefield')
    inputemail = StringField("Enter your Email", validators=[
                             DataRequired()], id='emailfield')
    inputpassworda = StringField("Enter your Password", validators=[
                                 DataRequired()], id='passwordfielda')
    inputpasswordb = StringField("Confirm your Password", validators=[
                                 DataRequired()], id='passwordfieldb')
    submit = SubmitField("Submit")


# signin FlaskForm
class SigninForm(FlaskForm):
    name = StringField("Enter your Username", validators=[
        DataRequired()], id='snamefield')
    passw = StringField("Enter your Password", validators=[
                        DataRequired()], id='spassfield')
    submit = SubmitField("Submit")


# create routes index first
@app.route('/')
def index():
    return redirect(url_for('home'))


# homepage route
@app.route('/homepage')
def home():
    return render_template('homepage.html', title='Home')


# signin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    # define variables
    session['name'] = None
    session['passw'] = None
    updated_users = Patrons.query.order_by(Patrons.date)
    # instantiate signin form
    signinform = SigninForm()
    # form data validation check (if submit button is pressed, and data is valid, execute code)
    if signinform.validate_on_submit():
        session['name'] = signinform.name.data
        session['passw'] = signinform.passw.data
        # add logic to check if user/pass exists in database #if user exists, if user does not exist, redirect to signup page
        ###### having issue with checking database for user/pass info ######
        for x in updated_users:
            if session['name'] == x.username and session['passw'] == x.password:
                return redirect(url_for('main')), session['name'], session['passw']
            return redirect(url_for('signup')), session['name']

    return render_template('signin.html',
                           title='Sign In',
                           name=session['name'],
                           signinform=signinform)


# create routes for error pages
# client side - page not found error
@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html'), 404


# server side errpr
@app.errorhandler(500)
def page_notfound(e):
    return render_template('500.html'), 500


# render about page
@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

###### This will be where users can access their account information ######
# placeholder for now of homepage #


@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('homepage.html',
                           title='Home')
#######################################################################


# render signup page for new users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # define variables
    session['username'] = None
    session['email'] = None
    session['passworda'] = None
    session['passwordb'] = None
    session['date'] = None
    session['password'] = None
    # instantiate signup form
    signupform = SignupForm()
    # this grabs the user input from the previous page, if entered. if not, the user will be "Guest"
    if session['name'] == None:
        session['name'] = 'Guest'
    else:
        pass
    # form data validation check (if submit button is pressed, and data is valid, execute code)
    if signupform.validate_on_submit():
        email = Patrons.query.filter_by(
            email=signupform.inputemail.data).first()
        # check if email already exists in database and passwords match.
        if email is None and signupform.inputpassworda.data == signupform.inputpasswordb.data:
            session['password'] = signupform.inputpassworda.data
            username = Patrons(username=signupform.inputusername.data, email=signupform.inputemail.data, passworda=signupform.inputpassworda.data,
                               passwordb=signupform.inputpasswordb.data, password=signupform.inputpassworda.data, date=datetime.now())
            sqldb.session.add(username)
            sqldb.session.commit()
            return redirect(url_for('main'))
        # error message for non-matching passwords
        elif email is None and signupform.inputpassworda.data != signupform.inputpasswordb.data:
            flash('Passwords do not match. Please try again.', 'danger')
        # error message for existing email
        elif email is not None:
            flash('Email already exists. Please try again.', 'danger')
    # query database for all users ordered by signup date
    updated_users = Patrons.query.order_by(Patrons.date)
    return render_template('signup.html', title='Sign Up', signupform=signupform, updated_users=updated_users)


@app.route('/allusers', methods=['GET', 'POST'])
def allusers():
    # administrative page to view all users in database -- only use for troubleshooting database -- not for production
    updated_users = Patrons.query.order_by(Patrons.date)
    return render_template('allusers.html', title='All Users', updated_users=updated_users)


@app.route('/main', methods=['GET', 'POST'])
def main():
    # this will be the main page for the user after successfully logging in
    return render_template('main.html', title='Main')


if __name__ == '__main__':
    # run the app -- debug mode is on -- not for production -- turn off debug mode for production
    app.run(debug=True)
