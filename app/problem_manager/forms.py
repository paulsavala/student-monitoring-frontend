from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l
from app.models import Course


class ProblemForm(FlaskForm):
    problem = TextAreaField(_l('Problem'),
                            render_kw={"placeholder": "You can type LaTeX code or plain text here. For LaTeX, use \[...\] or $$...$$ for multiline, and \(...\) for in-line."},
                            validators=[DataRequired()])
    notes = TextAreaField(_l('Notes'), render_kw={"placeholder": "Notes for yourself/other instructors"})
    solution = TextAreaField(_l('Solution'), render_kw={"placeholder": "Solution or notes about solving this problem"})
    course = SelectField(_l('Course'), coerce=int)
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_problem=None, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.course.choices = [(c.id, f'{c.subject} {c.number} - {c.title}')
                                for c in Course.query.order_by(Course.number.asc())]
        if original_problem is not None:
            self.problem.data = original_problem.body
            self.notes.data = original_problem.notes
            self.solution.data = original_problem.solution
            self.course.data = original_problem.course


class ProblemExplorerForm(FlaskForm):
    course = SelectMultipleField(_l('Course'), coerce=int)
    has_solution = BooleanField(_l('Must have solution'), default=False)
    has_notes = BooleanField(_l('Must have notes'), default=False)
    submit = SubmitField(_l('Search'))

    def __init__(self, *args, **kwargs):
        super(ProblemExplorerForm, self).__init__(*args, **kwargs)
        self.course.choices = [(c.id, f'{c.subject} {c.number} - {c.title}')
                                for c in Course.query.order_by(Course.number.asc())]
