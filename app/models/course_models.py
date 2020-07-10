from app import db


class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    department_short_name = db.Column(db.String(16), index=True)
    number = db.Column(db.Integer, index=True)

    # Parents
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    # Children
    course_instances = db.relationship('CourseInstances', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.lms_id)
