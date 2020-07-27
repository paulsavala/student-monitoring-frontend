from app import create_app, cli, db
from app.models import Schools, CollegeOf, Departments, Courses, Instructors

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'School': Schools,
            'CollegeOf': CollegeOf,
            'Department': Departments,
            'Course': Courses,
            'Instructor': Instructors}


cli.register(app)
