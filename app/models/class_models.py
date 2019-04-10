from app import db


# Mathematics, Computer Science, etc
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, index=True, unique=True)
    short_title = db.Column(db.String(16), nullable=False, unique=True)  # Short abbreviation, i.e MATH, CS, STATS, etc

    courses = db.relationship('Course', backref='subject', lazy='dynamic')
    classes = db.relationship('Class', backref='subject', lazy='dynamic')

    def __repr__(self):
        return '<Subject {}>'.format(self.title)


# Calculus I, Linear Algebra, etc (independent of the institution)
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, index=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    classes = db.relationship('Class', backref='course', lazy='dynamic')
    problems = db.relationship('Problem', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.title)


# "MATH123 Single-variable Calculus" (specific instance of a course at an institution)
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, index=True)
    number = db.Column(db.String(64), nullable=False, index=True)
    description = db.Column(db.String(1024))
    active = db.Column(db.Boolean, default=True, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), index=True, nullable=False)

    problems = db.relationship('Problem', backref='class', lazy='dynamic')

    def __repr__(self):
        return '<Class {}>'.format(self.title)
