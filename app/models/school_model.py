from app import db


class Schools(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    city = db.Column(db.String(128), index=True)
    state = db.Column(db.String(2), index=True)

    # Children
    college_of = db.relationship('CollegeOf', backref='school', lazy='dynamic')
    department = db.relationship('Departments', backref='school', lazy='dynamic')
    instructor = db.relationship('Instructors', backref='school', lazy='dynamic')

    def __repr__(self):
        return '<School {}>'.format(self.name)
