import os


basedir = os.path.abspath(os.path.dirname(__file__))


class GenericConfig:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'fj432f(#2rjcL%29j#26Pji3#$j09'
    ADMINS = ['psavala@stedwards.edu']
    LANGUAGES = ['en', 'es']
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://' + os.path.join(basedir, 'app.db')


class StEdwardsConfig(GenericConfig):
    # id in schools database table
    SCHOOL_ID = 1

    # URL for the LMS
    API_URL = 'https://student-monitoring-lms-api.herokuapp.com/v1.0'

    SEASON = 'Fall'
    YEAR = 2020
    SEMESTER = f'{SEASON} {YEAR}'


class StEdwardsTestConfig(StEdwardsConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' + os.path.join(basedir, 'app.db')
