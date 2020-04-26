from app import app
from flask import render_template, redirect, flash, url_for, request  # flask
from app.forms import LoginForm, SignupForm, TickerForm, InvestmentForm, DeleteForm, EditForm  # forms
from app.models import *
from app.charts import *
from werkzeug.security import generate_password_hash, check_password_hash  # sha256

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


@app.route('/dashboard/', methods=['GET', 'POST'])  # dashboard requires login
@login_required  # decorater - redirect to login page if not logged in
def dashboard():
    i, d, e = InvestmentForm(), DeleteForm(), EditForm()
    if i.validate_on_submit():
        if i.date_start.data <= date.today():
            try:
                isymbol = i.symbol.data
                iamount = i.amount.data
                tickerData = yf.Ticker(isymbol)
                info = tickerData.info
                idate_start = i.date_start.data
                new_investment = Investment(
                    symbol=isymbol, amount=iamount, date_start=idate_start, date_end=None)
                current_user.portfolio.append(new_investment)
                db.session.add(new_investment)
                db.session.commit()
                flash("New investment added!")
            except:
                flash("No data found, symbol may have been delisted!")
        else:
            flash("Must not be a future date!")
    if d.validate_on_submit():
        try:
            inv_id = d.d_id.data
            rem = Investment.query.filter_by(id=inv_id).first()
            db.session.delete(rem)
            db.session.commit()
            flash("Investment deleted successfully!")
        except:
            flash("INVALID ID!")

    if e.validate_on_submit():
        try:
            chosen_id, dend = e.e_id.data, e.e_date_end.data
            chem = Investment.query.filter_by(id=chosen_id).first()
            chem.date_end = dend
            db.session.commit()
            flash("End date updated successfully!")
        except:
            flash("ERROR")
    inv = Investment.query.filter_by(user_id=current_user.id).all()
    scriptpie, divpie = components(create_piechart(inv))
    profit = []
    for x in inv:
        tickerSymbol = x.symbol
        tickerData = yf.Ticker(tickerSymbol)
        if x.date_end != None:
            tickerDf = tickerData.history(start=x.date_start, end=x.date_end)
        else:
            tickerDf = tickerData.history(start=x.date_start)
        cprice = tickerDf['Close']
        price1 = float(cprice[cprice.index[0]])
        price2 = float(cprice[cprice.index[-1]])
        percent = ((price2 - price1) / price1) * 100
        profit.append(percent)


    lst = []
    for a in bubblesort_date(inv):
        if a.symbol not in lst:
            lst.append(a.symbol)
    data = yf.download(" ".join(lst), start=inv[0].date_start, end=date.today(),
                       group_by="ticker")

    scriptnum, divnum = components(create_numberofinvestmentschart(inv))
    scriptval, divval = components(create_portfoliovalue(inv,data))
    scriptbar, divbar = components(create_barchart(inv,data))

    return render_template("dashboard.html", title="Dashboard", form=i, form2=d, form3=e, inv=inv, profit=profit, scriptpie=scriptpie, divpie=divpie, scriptnum=scriptnum, divnum=divnum, scriptval=scriptval, divval=divval,scriptbar  = scriptbar, divbar =divbar)


@app.route('/research/', methods=['GET', 'POST'])
def research():
    t = TickerForm()
    script, div, info, tickerSymbol = "No chart data", "", "", "None"
    if t.validate_on_submit():
        try:
            tickerSymbol = t.t_symbol.data
            tickerData = yf.Ticker(tickerSymbol)
            tickerDf = tickerData.history(period='max')  # data frame
            y = tickerDf['Close']
            x = tickerDf.index
            #tickerDf.reset_index(inplace=True, drop=False)
            script, div = components(create_pricechart(x, y))
            info = tickerData.info
        except:
            flash("No data found, symbol may have been delisted!")
    return render_template("research.html", title="Research", form=t, script=script, div=div, info=info, symbol=tickerSymbol)


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
