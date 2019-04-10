from app import db
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


documents = db.Table(
    'documents',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'))
)


document_problems = db.Table(
    'document_problems',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id')),
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.id')),
)


starred = db.Table(
    'starred',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'))
)