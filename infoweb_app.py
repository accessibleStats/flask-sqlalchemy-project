from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# instantiate the application
app = Flask(__name__)
# generate secret key to prevent CSRF attacks
app.config['SECRET_KEY'] = "secret"

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

1
2
3
4
5
6
7
8
9
10
11
12