import os
basedir = os.path.abspath(os.path.dirname(__file__)) #base directory


class Config(object):  #Inherit from object class
    RECAPTCHA_PUBLIC_KEY = '' #Recaptcha keys
    RECAPTCHA_PRIVATE_KEY = ''
    DEBUG = False  #debug
    TESTING = False  #testing
    ENV = 'production'  #environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey1' #secret key for flask session
    SESSION_COOKIE_SECURE = True  #secure session
    SQLALCHEMY_TRACK_MODIFICATIONS = False  #disable verbose logging
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')  # database directory
    SQLALCHEMY_ECHO = False  #log and __repr__ all statements
    WTF_CSRF_ENABLED = True  # CSRF - Cross-site Registry Forgery
    WTF_CSRF_SECRET_KEY = os.environ.get(
        'WTF_CSRF_SECRET_KEY') or 'secretkey2'  #secret key for CSRF


class ProductionConfig(Config):  # For deployment, inherits from Config class
    pass


class DevelopmentConfig(Config):  # For development, inherits from Config class
    DEBUG = True #automatically update app when code is edited
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True
    ENV = 'development'


class TestingConfig(Config):  # For testing, inherits from Config class
    TESTING = True #activate test helpers that have an additional runtime cost
    SESSION_COOKIE_SECURE = False
