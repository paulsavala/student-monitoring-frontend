from app import db


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    city = db.Column(db.String(256), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    type = db.Column(db.String(256), nullable=False) # Should be one of 'COLLEGE', 'COMPANY'

    users = db.relationship('User', backref='institution', lazy='dynamic')
    classes = db.relationship('Class', backref='institution', lazy='dynamic')

    def __repr__(self):
        return '<Institution {}>'.format(self.name)