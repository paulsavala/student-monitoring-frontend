from app import create_app, cli, db
from app.models import Schools, CollegeOf, Departments, Course, CourseInstance, Instructor

app = create_app()
app.ssl_context = 'adhoc'


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'School': Schools,
            'CollegeOf': CollegeOf,
            'Department': Departments,
            'Course': Course,
            'CourseInstance': CourseInstance,
            'Instructor': Instructor}


cli.register(app)
