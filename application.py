from app import create_app, db, cli
from app.models import User, Problem, Message, Notification, Subject, Course, Institution, Class, Document

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'Message': Message, 'Notification': Notification,
            'Course': Course, 'Class': Class, 'Institution': Institution, 'Document': Document}

def create_first_user(app):
    with app.app_context():
        admin_user = User.query.filter_by(admin=True).first()
        if admin_user is not None:
            return True
        else:
            app.logger.info('Creating initial admin user')
            st_edwards = Institution(name="Saint Edward's University", city="Austin", state="TX", type="COLLEGE")

            admin_user = User(
                            username = 'admin',
                            email = 'problematic-admin@gmail.com',
                            first_name = 'Admin',
                            last_name = 'Admin',
                            full_name = 'Admin',
                            institution_id = 1,
                            admin = True
                            )
            admin_user.set_password('kickflip')

            db.session.add(st_edwards)
            db.session.add(admin_user)

            db.session.commit()

create_first_user(app)
