from flask import Flask  #micro web application library
from flask_sqlalchemy import SQLAlchemy #Object-relational mapper (ORM)
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user #User/Login sessions
from config import * #import configurations

app = Flask(__name__, template_folder="templates", static_folder="static") #creates an instance of Flask class
app.config.from_object('config.DevelopmentConfig')  #environment (development/production/...)
db = SQLAlchemy(app)  #Database

# User/Login session management
login_manager = LoginManager() #Initialization
login_manager.init_app(app) #Instantiation
login_manager.login_view = "login" #Redirect to login page if not logged in
login_manager.login_message = "You need to be signed in." #Message if not logged in
login_manager.login_message_category = "info" #Type of message

#To avoid circular import error/circular dependency, import code was put here
from app import routes, models

db.create_all()  #Database and tables creation
