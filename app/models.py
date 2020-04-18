from app import *
from datetime import date #classes for manipulating dates


# inherits from Model class (base class for all models in Flask SQLAlchemy)
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    passwordhashed = db.Column(db.String(80), nullable=False)
    portfolio = db.relationship('Investment', backref='user', lazy=True)

    def __init__(self, email, passwordhash):
        self.email = email
        self.passwordhashed = passwordhash

    def is_authenticated(self):
        return True

    def is_active(self, mail):
        active_user = User.query.filter_by(email=mail).first()
        if active_user:
            return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # all strings are stored as Unicode in an instance of the str type
        return str(self.id)

    def __repr__(self):
        return f'<User {self.id}>'

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, symbol, date_start, date_end):
        self.symbol = symbol
        self.date_start = date_start
        self.date_end = date_end

    def __repr__(self):
        return f'<Investment {self.id}>'
