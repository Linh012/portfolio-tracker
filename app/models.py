from app import * #import external libraries such as flask_sqlalchemy or flask_login

class User(UserMixin, db.Model): #inherits from UserMixin and Model class (base class for all models in Flask SQLAlchemy)
    __tablename__ = "user" #table name

    id = db.Column(db.Integer, primary_key=True) #primary key id
    email = db.Column(db.String(255), index=True, unique=True, nullable=False) #Cannot be null, needs to be unique, max length 255 characters
    passwordhashed = db.Column(db.String(80), nullable=False) #Cannot be null, max length 80 characters
    portfolio = db.relationship('Investment', backref='user', lazy=True) #one to many relationship with investment

    def __init__(self, email, passwordhash): #Constructor method
        self.email = email
        self.passwordhashed = passwordhash

    #Class methods
    def is_authenticated(self):
        return True

    def is_active(self, mail): #Query database for user
        active_user = User.query.filter_by(email=mail).first()
        if active_user:
            return True

    def is_anonymous(self):
        return False

    def get_id(self): #Get object id
        return str(self.id)
        #All strings are stored as Unicode in an instance of the str type

    def __repr__(self):
        return f'<User {self.id}>' #f-strings

class Investment(db.Model): #inherits from Model class
    id = db.Column(db.Integer, primary_key=True) #primary key id
    symbol = db.Column(db.String(5), nullable=False) #ticker symbol, max length 5 characters, cannot be null
    amount = db.Column(db.Float, nullable=False) #amount, cannot be null
    date_start = db.Column(db.Date, nullable=False) #start date, cannot be null
    date_end = db.Column(db.Date, nullable=True) #end date, can be null (investment active)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) #foreign key, cannot be null

    def __init__(self, symbol, amount, date_start, date_end): #Constructor method
        self.symbol = symbol
        self.amount = amount
        self.date_start = date_start
        self.date_end = date_end

    #Class methods
    def __repr__(self):
        return f'<Investment {self.id}>'
