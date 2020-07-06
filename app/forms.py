from flask_wtf import FlaskForm, RecaptchaField #Form fields and form validators
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm): #Login fields, inherits from FlaskForm class
    email = StringField('Email', validators=[
                        DataRequired(), Length(max=255), Email(message=('Invalid Email Address.'))]) #Email field, max length 255 characters
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(max=80)]) #Passworld field, max length 80 characters
    remember_me = BooleanField('Remember Me') #Boolean field, saves cookie on user's computer
    recaptcha = RecaptchaField() #Google's recaptcha v2 human verification service
    submit = SubmitField('Login') #Submit field


class SignupForm(FlaskForm): #Registration fields, inherits from FlaskForm class
    email = StringField('Email', validators=[
                        DataRequired(), Length(max=255), Email(message=('Invalid Email Address.'))]) #Email field, max length 255 characters
    password = PasswordField('Password', validators=[DataRequired(
        message=('Please enter a password.')), Length(max=80)]) #Passworld field, max length 80 characters
    recaptcha = RecaptchaField() #Google's recaptcha v2 human verification service

class TickerForm(FlaskForm): #Research page fields, inherits from FlaskForm
    t_symbol = StringField('Ticker Symbol', validators=[
                        DataRequired(), Length(max=5)]) #String field, max length 5 characters

#Dashboard page fields
class InvestmentForm(FlaskForm): #Add investment to database. inherits from FlaskForm class
    symbol = StringField('Ticker Symbol', validators = [DataRequired(), Length(max=10)])
    amount = FloatField('Amount', validators = [DataRequired()]) #Float field
    date_start = DateField('YY-MM-DD', format = '%Y-%m-%d', validators = [DataRequired()]) #Date field

class DeleteForm(FlaskForm): #Delete investment from database, inherits from FlaskForm class
    d_id = IntegerField('inv_id', validators = [DataRequired()]) #Integer field

class EditForm(FlaskForm): #Edit date_end of an investment in database
    e_id = IntegerField('ID', validators = [DataRequired()]) #Integer field, id of investment
    e_date_end = DateField('YY-MM-DD', format = '%Y-%m-%d') #Date field

#Settings page fields
class ChangePasswordForm(FlaskForm):
    cpassword = PasswordField('Password', validators=[DataRequired(
        message=('Please enter a password.')), Length(max=80)]) #Passworld field, max length 80 characters

class ChangeEmailForm(FlaskForm):
    cemail = StringField('Email', validators=[
                        DataRequired(), Length(max=255), Email(message=('Invalid Email Address.'))]) #Email field, max length 255 characters
