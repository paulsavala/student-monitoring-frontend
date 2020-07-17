from app import db


class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    lms_id = db.Column(db.String(1024))
    season = db.Column(db.String(64))
    year = db.Column(db.Integer)
    short_name = db.Column(db.String(64))
    long_name = db.Column(db.String(256))
    is_monitored = db.Column(db.Boolean, default=False)
    auto_email = db.Column(db.Boolean, default=False)

    # Parents
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    def __repr__(self):
        return '<Course {}>'.format(self.short_name)
