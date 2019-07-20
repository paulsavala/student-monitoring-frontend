import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from app.utils.utils import read_from_s3

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
admin = Admin()

def create_app():
    print('Creating app...')

    set_env_variables()

    from config import DevConfig, ProdConfig

    if os.environ.get("APP_ENV") == "prod":
        config_class = ProdConfig
    else:
        config_class = DevConfig
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    from app.models import User, Problem, Subject, Course, Class, Institution, Document
    with app.app_context():
        print(os.environ.get("DATABASE_URL"))
        print(config_class.SQLALCHEMY_DATABASE_URI)
        db.create_all()
        db.session.commit()
    if test_db():
        create_first_user()

    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    admin.init_app(app)

    app.elasticsearch = Elasticsearch([app.config.get('ELASTICSEARCH_URL')]) \
        if app.config.get('ELASTICSEARCH_URL') else None

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.problem_manager import bp as problem_manager_bp
    app.register_blueprint(problem_manager_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config.get('MAIL_SERVER'):
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Application Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config.get('LOG_TO_STDOUT'):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/application.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        print('app created')

    return app

def set_env_variables():
    print('Setting environment variables...')
    env_variables = read_from_s3(bucket=f'problematic-{os.environ.get("APP_ENV", "dev")}-us-east-1',
                                 key=f'configuration/{os.environ.get("APP_ENV", "dev")}-env-variables.json',
                                 as_dict=True)

    for k, v in env_variables.items():
        os.environ[k.upper()] = v
        print(f"Set os.environ['{k.upper()}']")

    db_creds = read_from_s3(bucket=f'problematic-{os.environ.get("APP_ENV", "dev")}-us-east-1',
                            key=f'credentials/{os.environ.get("APP_ENV", "dev")}-database.json',
                            as_dict=True, ignore_missing=True)
    if db_creds is not None:
        db_conn_str = f'{db_creds["connection"]}://{db_creds["username"]}:{db_creds["password"]}@{db_creds["host"]}:{db_creds["port"]}/{db_creds["database"]}'
        os.environ['DATABASE_URL'] = db_conn_str
        print(f"Set os.environ['DATABASE_URL'] to {os.environ['DATABASE_URL']}")

def test_db():
    print('Testing db connection...')
    with app.app_context():
        try:
            current_app.db.session.query("1").from_statement("SELECT 1").all()
            print('DB connection succeeded')
            return True
        except Exception as e:
            print('DB connection failed')
            print(e)
            return False

def create_first_user():
    with app.app_context():
        from app.models import User, Problem, Subject, Course, Class, Institution, Document

        db = current_app.db
        admin_user = User.query.filter_by(admin=True).first()

        if admin_user is None and os.environ.get('WERKZEUG_RUN_MAIN', 'false') == 'false':
            app.logger.info('Creating initial admin user')

            st_edwards = Institution(name="Saint Edward's University", city="Austin", state="TX", type="COLLEGE")

            bucket = f'problematic-{os.environ.get("APP_ENV", "dev")}-us-east-1'
            key = f'credentials/{os.environ.get("APP_ENV", "dev")}-credentials.json'
            admin_credentials = read_from_s3(bucket=bucket, key=key, as_dict=True)

            admin_user = User(
                            username = admin_credentials['username'],
                            email = admin_credentials['email'],
                            first_name = admin_credentials['first_name'],
                            last_name = admin_credentials['last_name'],
                            full_name = admin_credentials['full_name'],
                            institution_id = admin_credentials['institution_id'],
                            admin = admin_credentials['admin']
                            )
            admin_user.set_password(admin_credentials['password'])

            db.session.add(st_edwards)
            db.session.add(admin_user)
            db.session.commit()

            app.logger.info('Admin user created')
        else:
            app.logger.info('Admin user already exists')

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

# Flask-Admin setup
from app.models import User, Problem, Subject, Course, Class, Institution, Document

class RestrictedView(ModelView):
    column_exclude_list=('password_hash',)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

admin.add_view(RestrictedView(User, db.session))
admin.add_view(RestrictedView(Problem, db.session))
admin.add_view(RestrictedView(Institution, db.session))
admin.add_view(RestrictedView(Class, db.session))
admin.add_view(RestrictedView(Course, db.session))
admin.add_view(RestrictedView(Subject, db.session))
admin.add_view(RestrictedView(Document, db.session))
admin.add_link(MenuLink(name='Public Website', category='', url='/'))
