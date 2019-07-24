from app import create_app, cli, db
from app.models import User, Problem, Message, Notification, Subject, Course, Institution, Class, Document

import os

app = create_app()

# def create_first_user():
#     with app.app_context():
#         from app.models import User, Problem, Subject, Course, Class, Institution, Document
#
#         admin_user = User.query.filter_by(admin=True).first()
#
#         if admin_user is None and os.environ.get('WERKZEUG_RUN_MAIN', 'false') == 'false':
#             app.logger.info('Creating initial admin user')
#
#             st_edwards = Institution(name="Saint Edward's University", city="Austin", state="TX", type="COLLEGE")
#
#             admin_user = User(
#                             username = os.environ['ADMIN_USERNAME'],
#                             email = os.environ['ADMIN_EMAIL'],
#                             first_name = os.environ['ADMIN_FIRST_NAME'],
#                             last_name = os.environ['ADMIN_LAST_NAME'],
#                             full_name = os.environ['ADMIN_FULL_NAME'],
#                             institution_id = os.environ['ADMIN_INSTITUTION_ID'],
#                             admin = True
#                             )
#             admin_user.set_password(os.environ['ADMIN_PASSWORD'])
#
#             db.session.add(st_edwards)
#             db.session.add(admin_user)
#             db.session.commit()
#
#             app.logger.info('Admin user created')
#         else:
#             app.logger.info('Admin user already exists')
#
#
# create_first_user()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'Message': Message, 'Notification': Notification,
            'Course': Course, 'Class': Class, 'Institution': Institution, 'Document': Document}


cli.register(app)
