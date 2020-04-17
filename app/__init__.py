from flask import Flask  #external libraries/other imports
from flask_sqlalchemy import SQLAlchemy #Object-relational mapper (ORM)
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user #User/login sessions
from config import *

# Initialization/Instantiation of extensions/...
# creates an instance of Flask class
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object('config.DevelopmentConfig')  #environment (development/production/...)
db = SQLAlchemy(app)  # Database

# User session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You need to be signed in."
login_manager.login_message_category = "info"

from app import routes, models  # routes.py, models.py

db.create_all()  # Database + tables creation
