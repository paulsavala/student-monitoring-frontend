from app import db


class CourseInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lms_id = db.Column(db.String(1024), index=True, unique=True)
    season = db.Column(db.String(64))
    year = db.Column(db.Integer())
    section = db.Column(db.String(64))

    # Parents
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __repr__(self):
        return '<Course Instance {}>'.format(self.lms_id)
