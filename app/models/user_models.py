from datetime import datetime
from hashlib import md5
import json
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.models.problem_models import Problem
from app.models.message_models import Message, Notification
from app.models.base_models import starred, documents


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(256))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    title = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    admin = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))

    problems = db.relationship('Problem', backref='author', lazy='dynamic')
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    starred = db.relationship('Problem',
                                secondary=starred,
                                backref='users',
                                lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # ---- Password functions ----
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # ---- Followers functions ----
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # ---- Starred functions ----
    def is_starred(self, problem):
        is_starred = self.starred.filter(
            starred.c.problem_id == problem.id).count() > 0
        return is_starred

    def add_star(self, problem):
        if not self.is_starred(problem):
            self.starred.append(problem)

    def remove_star(self, problem):
        if self.is_starred(problem):
            self.starred.remove(problem)

    def starred_problems(self):
        return Problem.query.join(
                starred, (starred.c.problem_id == Problem.id)).filter(
                    starred.c.user_id == self.id).order_by(
                    Problem.created_ts.desc())

    # ---- Document functions ----
    def has_document(self, document):
        has_document = self.documents.filter(
            documents.c.document_id == document.id).count() > 0
        return has_document

    def add_document(self, document):
        if not self.is_starred(document):
            self.starred.append(document)

    def remove_document(self, document):
        if self.has_document(document):
            self.starred.remove(document)

    def is_in_document(self, problem, document=None):
        if document is None:
            for doc in self.documents:
                if doc.problems.filter(problem.id in [problem.id for problem in doc.problems]).count() > 0:
                    print(f'problem.id: {problem.id} is in document')
                    return True
        return False

    # ---- Misc functions ----
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n


@login.user_loader
def load_user(id):
    return User.query.get(int(id))