from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
