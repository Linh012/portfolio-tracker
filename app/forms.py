from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Length(max=120), Email(message=('Invalid Email Address.'))])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(max=80)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Length(max=120), Email(message=('Invalid Email Address.'))])
    password = PasswordField('Password', validators=[DataRequired(
        message=('Please enter a password.')), Length(max=80)])

class TickerForm(FlaskForm):
    symbol = StringField('Ticker Symbol', validators=[
                        DataRequired(), Length(max=10)])

class InvestmentForm(FlaskForm):
    symbol = StringField('Ticker Symbol', validators = [DataRequired(), Length(max=10)])
    amount = FloatField('Amount', validators = [DataRequired()])
    date_start = DateField('Start Date', format = '%Y-%m-%d', validators = [DataRequired()])

class DeleteForm(FlaskForm):
    id = IntegerField('inv_id', validators = [DataRequired()])

class EditForm(FlaskForm):
    id = IntegerField('ID', validators = [DataRequired()])
    date_end = DateField('End Date', format = '%Y-%m-%d')
