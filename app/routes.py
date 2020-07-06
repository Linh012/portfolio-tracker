from app import app
from flask import render_template, redirect, flash, url_for, request  # flask extensions
# import form classes
from app.forms import LoginForm, SignupForm, TickerForm, InvestmentForm, DeleteForm, EditForm, ChangeEmailForm, ChangePasswordForm
from app.models import *
from app.charts import *
# password hashing (sha256)
from werkzeug.security import generate_password_hash, check_password_hash

# Returns User object (instance of User) from database
@login_manager.user_loader
def load_user(uid):
    return User.query.filter(User.id == int(uid)).first()

# Home page/Index
@app.route('/')  # Function decorater - url
@app.route('/index/')
def index():
    return render_template("index.html", title="Home Page")

# Login page
# Accepts both GET and POST methods
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If already logged in, redirect to dashboard
        return redirect(url_for("dashboard"))
    f = LoginForm()
    if f.validate_on_submit():  # If login form valid and recaptcha passed
        existing_user = User.query.filter_by(
            email=f.email.data).first()  # Query database for user
        if existing_user:  # If user exists
            if check_password_hash(existing_user.passwordhashed, f.password.data):
                # If password corresponding to email is correct, create new login/user session
                login_user(existing_user, remember=f.remember_me.data)
                return redirect(url_for("dashboard"))  # Redirect to dashboard
            else:
                # If password incorrect, flash error message
                flash('Wrong password!')
        else:
            # If user not found in database, flash error message
            flash('Email not found in database!')

    # Render login page
    return render_template("login.html", title="Login Page", form=f)

# Sign up page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    s = SignupForm()
    if s.validate_on_submit():  # If sign up form valid and recaptcha passed
        email = s.email.data
        password = s.password.data
        existing_user = User.query.filter_by(
            email=email).first()  # Query database for user
        if existing_user is None:  # If user not found in database
            u = User(email=email, passwordhash=generate_password_hash(
                password, method='sha256')) # Hash password and create a new instance of user
            db.session.add(u)
            db.session.commit()  # Add new user to database
            flash('You have been registered successfully.')
            # flash success message and redirect to login page
            return redirect(url_for("login"))
        # If user already exists in database, flash error message
        flash('Email address is already registered.')
        return redirect(url_for("register")) # Redirect to sign up page
    # Render registration page
    return render_template("register.html", title="Registration Page", form=s)

#Dashboard page
@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required  # Function decorater - requires login/user session else redirects to login page
def dashboard():
    i, d, e = InvestmentForm(), DeleteForm(), EditForm()
    if i.validate_on_submit(): # If new investment submitted
        if i.date_start.data <= date.today(): # Validate start date (cannot be future date)
            try:
                isymbol = i.symbol.data # Retrieve data from forms
                iamount = i.amount.data
                tickerData = yf.Ticker(isymbol) # Web scrape Yahoo! Finance
                info = tickerData.info
                idate_start = i.date_start.data
                #Create an instance of investment
                new_investment = Investment(
                    symbol=isymbol, amount=iamount, date_start=idate_start, date_end=None)
                current_user.portfolio.append(new_investment)
                db.session.add(new_investment)
                db.session.commit() # Add new investment to database
                flash("New investment added!") # Flash success message
            except: # If ticker symbol not found on Yahoo! Finance, flash error message
                flash("No data found, symbol may have been delisted!")
        else: # If date in future, flash error message
            flash("Must not be a future date!")
    if d.validate_on_submit(): #If delete investment form submitted
        try:
            inv_id = d.d_id.data # Get id data from form
            # Query database for investment with submitted id
            rem = Investment.query.filter_by(id=inv_id).first()
            db.session.delete(rem)
            db.session.commit() # Delete investment and commit changes to database
            flash("Investment deleted successfully!")
        except: #If investment with specific id not found, flash error
            flash("INVALID ID!")

    if e.validate_on_submit(): #Edit end date
        try:
            chosen_id, dend = e.e_id.data, e.e_date_end.data # Retrieve data from forms
            chem = Investment.query.filter_by(id=chosen_id).first()
            # Query database for investment with submitted id
            chem.date_end = dend
            db.session.commit() #Set new end date to investment and commit changes to database
            flash("End date updated successfully!") # Flash success message
        except: #If investment not found, flash error message
            flash("INVALID ID!")

    # Query database for all investments
    inv = Investment.query.filter_by(user_id=current_user.id).all()

    #Profit calculation of every investment
    profit = []
    for x in inv: # For every investment
        tickerSymbol = x.symbol
        tickerData = yf.Ticker(tickerSymbol) # Web scrape Yahoo! Finance
        if x.date_end != None: # If investment is not active, limit unwanted data
            tickerDf = tickerData.history(start=x.date_start, end=x.date_end) # Data frame of ticker data
        else:
            tickerDf = tickerData.history(start=x.date_start)
        cprice = tickerDf['Close'] # Get close prices
        #Get price when investment initially was made and current price
        price1 = float(cprice[cprice.index[0]])
        price2 = float(cprice[cprice.index[-1]])
        percent = ((price2 - price1) / price1) * 100 # Calculate percentage change
        profit.append(percent) # Add to percent list

    lst = [] #List of unique ticker symbols
    for a in bubblesort_date(inv):
        if a.symbol not in lst: # If ticker symbol is unique, append to list
            lst.append(a.symbol)

    # Get data for multiple tickers at once and threads for faster completion
    data = yf.download(" ".join(lst), start=inv[0].date_start, end=date.today(),
                       group_by="ticker")

    #Graph generation
    scriptpie, divpie = components(create_piechart(inv)) # Create pie chart
    scriptnum, divnum = components(create_numberofinvestmentschart(inv)) # Create number of invesments chart
    scriptval, divval = components(create_portfoliovalue(inv, data)) # Create portfolio value chart
    scriptbar, divbar = components(create_barchart(inv, data)) # Create performance bar chart

    # Render page
    return render_template("dashboard.html", title="Dashboard", form=i, form2=d,
    form3=e, inv=inv, profit=profit, scriptpie=scriptpie, divpie=divpie, scriptnum=scriptnum,
    divnum=divnum, scriptval=scriptval, divval=divval, scriptbar=scriptbar, divbar=divbar)

# Research page
@app.route('/research/', methods=['GET', 'POST'])
def research():
    t = TickerForm()
    script, div, info, tickerSymbol = "No chart data", "", "", "None"
    if t.validate_on_submit(): # If form submitted
        try:
            tickerSymbol = t.t_symbol.data
            tickerData = yf.Ticker(tickerSymbol) # Web scrape Yahoo! Finance
            tickerDf = tickerData.history(period='max')  # Data frame of ticker data
            y = tickerDf['Close']
            x = tickerDf.index # Index of data frame are  dates
            #tickerDf.reset_index(inplace=True, drop=False)
            script, div = components(create_pricechart(x, y))
            info = tickerData.info # Other information about ticker
        except: # If ticker symbol not found on Yahoo! Finance, flash error message
            flash("No data found, symbol may have been delisted!")
    return render_template("research.html", title="Research", form=t,
    script=script, div=div, info=info, symbol=tickerSymbol)

#Logout page
@app.route('/logout/')
@login_required  # Needs to be logged in before you can be logged out
def logout():
    logout_user()  # Any cookies of user/login session will be cleaned up
    return redirect(url_for("index")) # Redirect to index/home page


@app.errorhandler(404)  # 404 error handling
def page_not_found_error(error): # Render error page
    return render_template("error.html", url=request.path, statuscode='404')


@app.errorhandler(500)  # 500 error handling
def internal_server_error(error): # Render error page
    return render_template("error.html", url=request.path, statuscode='500')

# About page
@app.route('/about/')
def about():
    return render_template("about.html", title="About")

# Settings page
@app.route('/settings/', methods=['GET', 'POST'])
@login_required # Requires to be logged in
def settings():
    pform, eform = ChangePasswordForm(), ChangeEmailForm()
    cid = current_user.get_id()
    existing_user = User.query.filter_by(
                id=cid).first()  # Query database for user
    if eform.validate_on_submit():
        try:
            existing_user.email = eform.cemail.data
            db.session.commit() #Set new email and commit changes to database
            flash("Email changed successfully!") # Flash success message
        except:
            flash("Error")
    if pform.validate_on_submit():
        try:
            existing_user.passwordhashed = generate_password_hash(
                pform.cpassword.data, method='sha256')
            db.session.commit() #Set new email and commit changes to database
            flash("Password changed successfully!") # Flash success message
        except:
            flash("Error")
    return render_template("settings.html", title="Settings", email=existing_user.email, pform = pform, eform = eform)
