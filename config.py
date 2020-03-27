# Configurations file
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):  # Parent class
    DEBUG = False  # debug
    TESTING = False  # testing
    ENV = 'production'  # environment
    # flask session requires secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey1'
    SESSION_COOKIE_SECURE = True  # secure session
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # disable verbose info
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')  # db location
    SQLALCHEMY_ECHO = False  # log and __repr__ all statements
    WTF_CSRF_ENABLED = True  # CSRF - Cross-site Registry Forgery
    WTF_CSRF_SECRET_KEY = os.environ.get(
        'WTF_CSRF_SECRET_KEY') or 'secretkey2'  # secretkey for CSRF


class ProductionConfig(Config):  # For deployment
    pass


class DevelopmentConfig(Config):  # For development
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True
    ENV = 'development'


class TestingConfig(Config):  # For testing
    TESTING = True
    SESSION_COOKIE_SECURE = False
