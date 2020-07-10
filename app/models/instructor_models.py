from app import db, login
from flask_login import UserMixin


class Instructors(db.Model, UserMixin):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    api_token = db.Column(db.String(256), index=True, unique=True)
    is_admin = db.Column(db.Boolean, index=True, default=False)
    is_registered = db.Column(db.Boolean, default=False)

    # Parents
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    # Children
    course_instances = db.relationship('CourseInstances', backref='instructor', lazy='dynamic')

    def __repr__(self):
        return '<Instructor {}>'.format(self.email)


@login.user_loader
def load_user(user_id):
    return Instructors.query.get(user_id)
