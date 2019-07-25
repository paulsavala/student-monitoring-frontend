from app import db
from app.models.base_models import SearchableMixin
from datetime import datetime
from app.models.document_models import Document


class Problem(SearchableMixin, db.Model):
    __searchable__ = ['body', 'notes', 'solution']
    id = db.Column(db.Integer, primary_key=True)
    latex = db.Column(db.String(10000), nullable=False)
    parsed_latex = db.Column(db.String(10000))
    notes = db.Column(db.String(5000))
    parsed_notes = db.Column(db.String(5000))
    solution = db.Column(db.String(5000))
    parsed_solution = db.Column(db.String(5000))
    image = db.Column(db.String(1024))
    created_ts = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    edited_ts = db.Column(db.DateTime)
    starred_count = db.Column(db.Integer, default=0)
    doc_count = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), index=True)

    def __repr__(self):
        return f'<Problem {self.id}>'

