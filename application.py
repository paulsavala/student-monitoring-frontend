from app import create_app, db, cli
from app.models import User, Problem, Message, Notification, Course, Institution

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem, 'Message': Message,
            'Course': Course, 'Institution': Institution, 'Notification': Notification}

if __name__ == '__main__':
    app.run()