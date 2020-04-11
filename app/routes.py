from app import app
from flask import render_template, redirect, flash, url_for, request #flask
from app.forms import LoginForm, SignupForm, TickerForm #keep this updated
from app.models import * #bad practice
from app.charts import *
from werkzeug.security import generate_password_hash, check_password_hash #sha256
import yfinance as yf  # YAHOO! FINANCE
import pandas as pd  # for data manipulation and analysis - data frame = 2 dimensional data structure
import datetime #date (format)

# Returns User object (instance of User) from db
@login_manager.user_loader
def load_user(uid):
    return User.query.filter(User.id == int(uid)).first()

# Home page/Index
@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html", title="Home Page")

# Login page
# accepts both GET and POST methods
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # if already logged in, redirect to dashboard
        return redirect(url_for("dashboard"))
    f = LoginForm()
    if f.validate_on_submit():  # data validation
        existing_user = User.query.filter_by(
            email=f.email.data).first()  # database query
        if existing_user:  # if match found
            if check_password_hash(existing_user.passwordhashed, f.password.data):
                # login/user session - redirect to dashboard
                login_user(existing_user, remember=f.remember_me.data)
                return redirect(url_for("dashboard"))
            else:
                flash('Wrong password!')
        else:
            flash('Email not found in database!')



    # render login page
    return render_template("login.html", title="Login Page", form=f)

# Sign up page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    s = SignupForm()
    if s.validate_on_submit():  # data validation
        email = s.email.data
        password = s.password.data
        existing_user = User.query.filter_by(
            email=email).first()  # database query
        if existing_user is None:  # if no match
            u = User(email=email, passwordhash=generate_password_hash(
                password, method='sha256'))
            db.session.add(u)
            db.session.commit()  # add and commit new user
            flash('You have been registered successfully.')
            # flash success message and redirect to login page
            return redirect(url_for("login"))
        # if found match, flash unsuccess message
        flash('Email address is already registered.')
        return redirect(url_for("register"))
    # render registration page
    return render_template("register.html", title="Registration Page", form=s)


@app.route('/dashboard/')  # dashboard requires login
@login_required  # decorater - redirect to login page if not logged in
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@app.route('/research/', methods=['GET', 'POST'])
def research():
    t = TickerForm()
    script,div,info,tickerSymbol = "No chart data", "", "","None"
    if t.symbol.data:
        try:
            tickerSymbol = t.symbol.data
            tickerData = yf.Ticker(tickerSymbol)
            tickerDf = tickerData.history(period='max')  # data frame
            print(tickerDf)
            y = tickerDf['Close']
            x = tickerDf.index
            #tickerDf.reset_index(inplace=True, drop=False)
            script,div = components(create_pchart(x,y))
            info = tickerData.info
        except:
            flash("No data found! Symbol may have been delisted!")
    return render_template("research.html", title="Research",form = t, script = script, div = div, info = info, symbol = tickerSymbol)


@app.route('/logout/')  # logout
@login_required  # needs to be logged in before you can be logged out
def logout():
    logout_user()  # any cookies for their session will be cleaned up
    return redirect(url_for("index"))


@app.errorhandler(404)  # 404 error handling
def page_not_found_error(error):
    return render_template("error.html", url=request.path, statuscode='404')


@app.errorhandler(500)  # 500 error handling
def internal_server_error(error):
    return render_template("error.html", url=request.path, statuscode='500')
