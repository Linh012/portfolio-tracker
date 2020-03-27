from app import *


# inherits from Model class (base class for all models in Flask SQLAlchemy)
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    passwordhashed = db.Column(db.String(80))

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
