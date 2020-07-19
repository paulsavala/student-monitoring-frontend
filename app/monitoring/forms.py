from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField


# Update course monitoring/auto email
class EditCoursesFlaskForm(FlaskForm):
    submit_changes = SubmitField('Submit changes')


# Helper function to dynamically build the form
def edit_courses_flask_form_builder(course_list):
    class ClassesFlaskForm(EditCoursesFlaskForm):
        courses = course_list

    for c in course_list:
        setattr(ClassesFlaskForm, f'is_monitored_{c}', BooleanField(label='Is monitored'))
        setattr(ClassesFlaskForm, f'short_name_{c}', StringField(label=c,
                                                                 render_kw={'readonly': True}))
        setattr(ClassesFlaskForm, f'auto_email_{c}', BooleanField(label='Auto email'))

    return ClassesFlaskForm()


# Refresh courses from LMS
class RefreshCoursesFlaskForm(FlaskForm):
    refresh_courses = SubmitField('Refresh courses')
