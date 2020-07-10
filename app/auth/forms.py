from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class RegisterFlaskForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=50)])
    department = SelectField(
        'Department',
        # choices are added dynamically based on departments in database
        coerce=int
    )
    api_token = StringField('API Token', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Register')
