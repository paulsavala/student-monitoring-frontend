import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from config import StEdwardsConfig as config_class

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.about'
mail = Mail()
bootstrap = Bootstrap()
admin = Admin()
talisman = Talisman()


def create_app():
    print('Creating app...')

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)

    # Talisman CSP settings
    csp = {
        'default-src': [
            '\'self\''
        ],
        'style-src': ['stackpath.bootstrapcdn.com',
                      'cdn.jsdelivr.net',
                      'student-monitoring-frontend.herokuapp.com'
                      ],
        'script-src': ['code.jquery.com',
                       'cdnjs.cloudflare.com',
                       'stackpath.bootstrapcdn.com',
                       'cdn.jsdelivr.net'
                       ],
        'font-src': ['use.fontawesome.com']
    }
    talisman.init_app(app, content_security_policy=csp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.monitoring import bp as monitoring_bp
    app.register_blueprint(monitoring_bp)

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


# Flask-Admin setup
from app.models import Schools, CollegeOf, Departments, Courses, Instructors


class RestrictedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


admin.add_view(RestrictedView(Schools, db.session))
admin.add_view(RestrictedView(CollegeOf, db.session))
admin.add_view(RestrictedView(Departments, db.session))
admin.add_view(RestrictedView(Courses, db.session))
admin.add_view(RestrictedView(Instructors, db.session))
admin.add_link(MenuLink(name='Public Website', category='', url='/'))
