from app import create_app, cli, db
from app.models import User, Problem, Message, Notification, Subject, Course, Institution, Class, Document
from app.utils.utils import read_from_s3

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'Message': Message, 'Notification': Notification,
            'Course': Course, 'Class': Class, 'Institution': Institution, 'Document': Document}
