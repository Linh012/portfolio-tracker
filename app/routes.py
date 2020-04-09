from app import app
from flask import render_template, redirect, flash, url_for, request #flask
from app.forms import LoginForm, SignupForm #keep this updated
from app.models import * #bad practice
from werkzeug.security import generate_password_hash, check_password_hash #sha256
import yfinance as yf  # YAHOO! FINANCE
import pandas as pd  # for data manipulation and analysis - data frame = 2 dimensional data structure
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool #graphing
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

#https://www.twitch.tv/healthygamer_gg/clip/TransparentInspiringHabaneroANELE
@app.route('/research/', methods=['GET'])
def research():
    tickerSymbol = 'ETH-USD'
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='max')  # data frame
    print(tickerDf['Close'])
    y = tickerDf['Close']
    x = tickerDf.index
    #tickerDf.reset_index(inplace=True, drop=False)
    tools = "pan,box_zoom,wheel_zoom,save,reset"

    # create a new plot with a title and axis labels
    p = figure(tools=tools,title="Price Chart", x_axis_type="datetime",
               x_axis_label='Datetime', y_axis_label='Price')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)
    hover = HoverTool()
    hover.tooltips = "<div style=padding=5px>Price:@y</div>"
    p.add_tools(hover)

    script,div = components(p)
    calendar = tickerData.calendar
    info = tickerData.info
    recommendations = tickerData.recommendations
    actions = tickerData.actions
    dividends = tickerData.dividends

    return render_template("research.html", title="Research", script = script, div = div, info = info)


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
