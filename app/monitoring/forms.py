from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, FieldList, FormField


class CourseFlaskForm(FlaskForm):
    lms_id = StringField(render_kw={'readonly': True})
    short_name = StringField(render_kw={'readonly': True})
    is_monitored = BooleanField()
    auto_email = BooleanField()


class EditCoursesFlaskForm(FlaskForm):
    courses = FieldList(FormField(CourseFlaskForm))

    submit_changes = SubmitField('Submit changes')
    refresh_courses = SubmitField('Refresh courses')
