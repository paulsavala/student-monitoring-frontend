from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class ProblemForm(FlaskForm):
    problem = TextAreaField(_l('Problem'),
                            render_kw={"placeholder": "You can type LaTeX code or plain text here. For LaTeX, use \[...\] or $$...$$ for multiline, and \(...\) for in-line."},
                            validators=[DataRequired()])
    notes = TextAreaField(_l('Notes'), render_kw={"placeholder": "Notes for yourself/other instructors"})
    solution = TextAreaField(_l('Solution'), render_kw={"placeholder": "Solution or notes about solving this problem"})
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_problem=None, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        if original_problem is not None:
            self.problem.data = original_problem.body
            self.notes.data = original_problem.notes
            self.solution.data = original_problem.solution


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))
