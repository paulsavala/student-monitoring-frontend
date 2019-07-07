from app import create_app, db, cli
from app.models import User, Problem, Message, Notification, Subject, Course, Institution, Class, Document
from app.utils.utils import read_from_s3

import boto3
import json
import os

def set_env_variables():
    # Avoid setting variables twice while in debug
    if os.environ.get('WERKZEUG_RUN_MAIN', 'false') == 'false':
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
            print("Set os.environ['DATABASE_URL']")

set_env_variables()

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'Message': Message, 'Notification': Notification,
            'Course': Course, 'Class': Class, 'Institution': Institution, 'Document': Document}

def create_first_user(app):
    with app.app_context():
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

create_first_user(app)
