from app import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    department = db.Column(db.Integer, index=True)
    number = db.Column(db.Integer, index=True)

    # Parents
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    # Children
    course_instances = db.relationship('CourseInstance')

    def __repr__(self):
        return '<Course {}>'.format(self.lms_id)
