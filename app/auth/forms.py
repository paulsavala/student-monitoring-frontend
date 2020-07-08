from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length


class RegisterForm(Form):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=50)])
    department = SelectField(
        'Department',
        validators=[InputRequired()],
        # choices are added dynamically based on departments in database
        coerce=int
    )
    api_token = StringField('API Token', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Register')
