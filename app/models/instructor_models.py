from app import db


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    api_token = db.Column(db.String(256), index=True, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, index=True, default=False)
    registered = db.Column(db.Boolean, default=False)

    # Parents
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    # Children
    course_instances = db.relationship('CourseInstance')

    def __repr__(self):
        return '<Instructor {}>'.format(self.email)
