from app import db


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    city = db.Column(db.String(128), index=True)
    state = db.Column(db.String(2), index=True)

    # Children
    college_of = db.relationship('CollegeOf')
    instructor = db.relationship('Instructor')

    def __repr__(self):
        return '<School {}>'.format(self.name)
