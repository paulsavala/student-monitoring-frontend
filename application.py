from app import create_app, cli, db
from app.models import School, CollegeOf, Department, Course, CourseInstance, Instructor

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'School': School,
            'CollegeOf': CollegeOf,
            'Department': Department,
            'Course': Course,
            'CourseInstance': CourseInstance,
            'Instructor': Instructor}


cli.register(app)
