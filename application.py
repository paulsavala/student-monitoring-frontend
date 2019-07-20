from app import create_app, cli, db
from app.models import User, Problem, Message, Notification, Subject, Course, Institution, Class, Document
from app.utils.utils import read_from_s3

import os

app = create_app()
cli.register(app)

def test_db():
    print('Testing db connection...')
    with app.app_context():
        try:
            db.session.query("1").from_statement("SELECT 1").all()
            print('DB connection succeeded')
            return True
        except Exception as e:
            print('DB connection failed')
            print(e)
            return False

def create_first_user():
    with app.app_context():
        from app.models import User, Problem, Subject, Course, Class, Institution, Document

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

if test_db():
    create_first_user()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'Message': Message, 'Notification': Notification,
            'Course': Course, 'Class': Class, 'Institution': Institution, 'Document': Document}
