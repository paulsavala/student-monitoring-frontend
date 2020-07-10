from app import db


class Departments(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    long_name = db.Column(db.String(128))
    short_name = db.Column(db.String(16))

    # Parents
    college_of_id = db.Column(db.Integer, db.ForeignKey('college_of.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    # Children
    instructor = db.relationship('Instructors', backref='department', lazy='dynamic')
    course = db.relationship('Courses', backref='department', lazy='dynamic')
    course_instance = db.relationship('CourseInstances', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department {}>'.format(self.long_name)
