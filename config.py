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
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    DEBUG = True


class StEdwardsConfig(GenericConfig):
    # id in schools database table
    school_id = 1

    # Connect to the database
    # todo: Remove after getting RDS online
    db_file = '../student_monitoring/app.db'

    # URL for the LMS
    lms_url = 'https://stedwards.instructure.com/'

    # URL for the student monitoring LMS API
    api_url = 'https://ve9e8bak70.execute-api.us-east-1.amazonaws.com/default'

    semester = 'Spring 2020'
