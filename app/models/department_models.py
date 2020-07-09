from app import db


class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_name = db.Column(db.String(128))
    short_name = db.Column(db.String(16), unique=True)

    # Parents
    college_of_id = db.Column(db.Integer, db.ForeignKey('CollegeOf.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('School.id'))

    # Children
    instructor = db.relationship('Instructor')
    course = db.relationship('Course')
    course_instance = db.relationship('CourseInstance')

    def __repr__(self):
        return '<Department {}>'.format(self.long_name)
