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

# account registration form class creation
class AccountForm(FlaskForm):
    inputname = StringField("Enter your Username", validators=[DataRequired()], id='namefield')
    submit = SubmitField("Login")

# signup form class creation
class SignupForm(FlaskForm):
    inputusername = StringField("Enter your Username", validators=[DataRequired()], id='usernamefield')
    inputemail = StringField("Enter your Email", validators=[DataRequired()], id='emailfield')
    inputpassworda = StringField("Enter your Password", validators=[DataRequired()], id='passwordfielda')
    inputpasswordb = StringField("Confirm your Password", validators=[DataRequired()], id='passwordfieldb')
    submit = SubmitField("Submit")

# create routes for various webpages
@app.route('/')
def index():
    return redirect(url_for('account'))

@app.route('/homepage')
def home():
    return render_template('homepage.html', title='Home')

# create routes for error pages
#client side - page not found error
@app.errorhandler(404)
def page_notfound(e):
    return render_template('404.html'), 404
#server side errpr
@app.errorhandler(500)
def page_notfound(e):
    return render_template('500.html'), 500

# render about page
@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/account', methods=['GET', 'POST'])
def account():
    session['name'] = None
    userform = AccountForm()
    updated_users = Patrons.query.order_by(Patrons.date)
    # form data validation check
    if userform.validate_on_submit():
        session['name']= userform.inputname.data
        #userform.inputname.data = ''
        # add logic to check if user/pass exists in database #if user exists, if user does not exist, redirect to signup page
        # logic does not work at this point - perhaps something wrong in for loop
        for x in updated_users:
            if session['name'] == x.username:
                return redirect(url_for('main')), session['name']
            return redirect(url_for('signup')), session['name']

    return render_template('account.html',
    title='Account Information',
    name = session['name'],
    userform = userform)

# render about page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session['username'] = None
    session['email'] = None
    session['passworda'] = None
    session['passwordb'] = None
    session['date'] = None
    session['password'] = None

    signupform = SignupForm()
    # form data validation check
    if session['name'] == None:
        session['name'] = 'Guest'
    else: pass

    if signupform.validate_on_submit():
        email = Patrons.query.filter_by(email=signupform.inputemail.data).first()
        if email is None and signupform.inputpassworda.data == signupform.inputpasswordb.data:
            session['password'] = session['passworda']
            username = Patrons(username=signupform.inputusername.data, email=signupform.inputemail.data, passworda=signupform.inputpassworda.data, passwordb=signupform.inputpasswordb.data, password=session['password'], date=datetime.now())
            sqldb.session.add(username)
            sqldb.session.commit()
            return redirect(url_for('main'))
        elif email is None and signupform.inputpassworda.data != signupform.inputpasswordb.data:
            flash('Passwords do not match. Please try again.', 'danger')
        elif email is not None:
            flash('Email already exists. Please try again.', 'danger')

    updated_users = Patrons.query.order_by(Patrons.date)
    return render_template('signup.html', title='Sign Up', signupform = signupform, updated_users = updated_users)

@app.route('/allusers', methods=['GET', 'POST'])
def allusers():
    updated_users = Patrons.query.order_by(Patrons.date)
    return render_template('allusers.html', title='All Users', updated_users = updated_users)

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html', title='Main')

if __name__=='__main__':
    app.run(debug=True)


# end of file