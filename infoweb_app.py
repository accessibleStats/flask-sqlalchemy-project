from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from aux import dburi, csrftoken



# instantiate the application
app = Flask(__name__)
# generate secret key to prevent CSRF attacks
app.config['SECRET_KEY'] = csrftoken
# specify database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = dburi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# declare database object
sqldb = SQLAlchemy(app)

# Website Patrons table
class Patrons(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    username = sqldb.Column(sqldb.String(100), nullable=False)
    email = sqldb.Column(sqldb.String(80), unique=True, nullable=False)
    passworda = sqldb.Column(sqldb.String(100), nullable=False)
    passwordb = sqldb.Column(sqldb.String(100), nullable=False)
    requesedfreq = sqldb.Column(sqldb.String(100), nullable=False)
    create_time = sqldb.Column(sqldb.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<{self.username} - {self.id}>'

# account registration form class creation
class AccountForm(FlaskForm):
    name = StringField("Enter your Username or Email Address", validators=[DataRequired()], id='namefield')
    submit = SubmitField("Submit")

# create routes for various webpages
@app.route('/')
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
    name = None
    userform = AccountForm()
    # form data validation check
    if userform.validate_on_submit():
        name= userform.name.data
        userform.name.data = ''

    return render_template('account.html',
    title='Account Information',
    name = name,
    userform = userform)

# render about page
@app.route('/signup')
def signup():
    return render_template('signup.html', title='Sign Up')

if __name__=='__main__':
    app.run(debug=True)


# end of file