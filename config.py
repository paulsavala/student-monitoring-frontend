import os

basedir = os.path.abspath(os.path.dirname(__file__))

class GenericConfig(object):
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'fj432f(#2rjcL%29j#26Pji3#$j09'
    ADMINS = ['problematic.web@gmail.com']
    LANGUAGES = ['en', 'es']
    PROBLEMS_PER_PAGE = 10
    TEMPLATE_DIR = os.path.join(basedir, 'app/latex_templates/')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

class DevConfig(GenericConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # os.environ['ADMIN_USERNAME'] = 'admin_dev'
    # os.environ['ADMIN_EMAIL'] = 'problematic.web@gmail.com'
    # os.environ['ADMIN_FIRST_NAME'] = 'Admin'
    # os.environ['ADMIN_LAST_NAME'] = 'Admin'
    # os.environ['ADMIN_FULL_NAME'] = 'Admin'
    # os.environ['ADMIN_INSTITUTION_ID'] = '1'
    # os.environ['ADMIN_PASSWORD'] = 'admin_dev_314159'

class ProdConfig(GenericConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
