from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, BooleanField, \
                    SelectMultipleField, StringField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User, Institution, Course, Class
from flask_login import current_user


class ProblemForm(FlaskForm):
    problem = TextAreaField(_l('Problem'),
                            render_kw={"placeholder": "You can type LaTeX code or plain text here. For LaTeX, use \[...\] or $$...$$ for multiline, and $...$ for in-line."},
                            validators=[DataRequired()])
    notes = TextAreaField(_l('Notes'), render_kw={"placeholder": "(Optional) Notes for yourself/other instructors"})
    solution = TextAreaField(_l('Solution'), render_kw={"placeholder": "(Optional) Solution or notes about solving this problem"})
    class_name = SelectField(_l('Class'), coerce=int)
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_problem=None, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.class_name.choices = [(c.id, f'{c.subject.short_title} {c.number} - {c.title}')
                                   for c in Class.query.filter(Class.institution_id==current_user.institution_id).order_by(Class.number.asc())]
        if original_problem is not None:
            self.problem.data = original_problem.latex
            self.notes.data = original_problem.notes
            self.solution.data = original_problem.solution
            self.class_name.data = original_problem.class_id


class ProblemExplorerForm(FlaskForm):
    search = StringField(_l('Search'), render_kw={"placeholder": "(Optional) Search terms"})
    course = SelectMultipleField(_l('Course'), coerce=int)
    author = SelectMultipleField(_l('Author'), coerce=int)
    institution = SelectMultipleField(_l('Institution'), coerce=int)
    has_solution = BooleanField(_l('Must have solution'), default=False)
    has_notes = BooleanField(_l('Must have notes'), default=False)
    submit = SubmitField(_l('Search'))

    def __init__(self, *args, **kwargs):
        super(ProblemExplorerForm, self).__init__(*args, **kwargs)
        self.course.choices = [(c.id, c.title) for c in Course.query]
        self.author.choices = [(0, 'All')] + [(a.id, f'{a.full_name} - {a.institution.name}') for a in User.query]
        self.institution.choices = [(0, 'All')] + [(i.id, f'{i.name} - {i.city}, {i.state}') for i in Institution.query]


class DocumentForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    class_name = StringField(_l('Class'), validators=[DataRequired()])
    submit = SubmitField(_l('Generate LaTeX'))
