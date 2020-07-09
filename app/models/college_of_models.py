from app import db


class CollegeOf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_name = db.Column(db.String(128))
    short_name = db.Column(db.String(16))

    # Parents
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    # Children
    department = db.Column('Department')

    def __repr__(self):
        return '<Department {}>'.format(self.long_name)
