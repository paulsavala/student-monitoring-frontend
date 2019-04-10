from app import db
from datetime import datetime
from app.models.base_models import document_problems


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    created_ts = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    problems = db.relationship('Problem',
                              secondary=document_problems,
                              backref='documents',
                              lazy='dynamic')

    def __repr__(self):
        return f'<Document {self.name}>'

    # ---- Document problem functions ----
    def has_problem(self, problem):
        has_problem = self.problems.filter(
            document_problems.c.problem_id == problem.id).count() > 0
        return has_problem

    def add_problem(self, problem):
        if not self.has_problem(problem):
            self.problems.append(problem)

    def remove_problem(self, problem):
        if self.has_problem(problem):
            self.problems.remove(problem)

    def clear_document(self):
        for problem in self.problems:
            self.problems.remove(problem)