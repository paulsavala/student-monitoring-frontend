from app import db


class CourseInstances(db.Model):
    __tablename__ = 'course_instances'
    id = db.Column(db.Integer, primary_key=True)
    lms_id = db.Column(db.String(1024), index=True, unique=True)
    season = db.Column(db.String(64))
    year = db.Column(db.Integer)
    section = db.Column(db.String(64))

    # Parents
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __repr__(self):
        return '<Course Instance {}>'.format(self.lms_id)
