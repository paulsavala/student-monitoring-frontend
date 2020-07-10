from app import db


class CollegeOf(db.Model):
    __tablename__ = 'college_of'
    id = db.Column(db.Integer, primary_key=True)
    long_name = db.Column(db.String(128))
    short_name = db.Column(db.String(16))

    # Parents
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    # Children
    department = db.relationship('Departments', backref='college_of', lazy='dynamic')

    def __repr__(self):
        return '<Department {}>'.format(self.long_name)
