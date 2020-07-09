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

    DB_RELATIVE_DIR = os.path.join(basedir, '../student_monitoring/app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite://' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/paulsavala/Coding/Projects/student_monitoring/app.db'


class StEdwardsConfig(GenericConfig):
    # id in schools database table
    SCHOOL_ID = 1

    # URL for the LMS
    LMS_URL = 'https://stedwards.instructure.com/'

    # URL for the student monitoring LMS API
    API_URL = 'https://ve9e8bak70.execute-api.us-east-1.amazonaws.com/default'

    SEMESTER = 'Spring 2020'

    # DEBUG = False
