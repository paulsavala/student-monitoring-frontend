from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, HiddenField


class EditCoursesFlaskForm(FlaskForm):
    submit_changes = SubmitField('Submit changes')
    refresh_courses = SubmitField('Refresh courses')
    test_email = SubmitField('Send test email')


def edit_courses_flask_form_builder(course_list):
    class ClassesFlaskForm(EditCoursesFlaskForm):
        num_courses = len(course_list)

    for i, course in enumerate(course_list):
        setattr(ClassesFlaskForm, f'is_monitored_{i}', BooleanField(label='Is monitored'))
        setattr(ClassesFlaskForm, f'short_name_{i}', StringField(label=course,
                                                                 render_kw={'readonly': True}))
        setattr(ClassesFlaskForm, f'auto_email_{i}', BooleanField(label='Auto email'))

    return ClassesFlaskForm()



