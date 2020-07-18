from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, FieldList, FormField, HiddenField


# class CourseFlaskForm(FlaskForm):
#     lms_id = HiddenField()
#     short_name = StringField()
#     is_monitored = BooleanField()
#     auto_email = BooleanField()


class EditCoursesFlaskForm(FlaskForm):
    submit_changes = SubmitField('Submit changes')
    refresh_courses = SubmitField('Refresh courses')


def edit_courses_flask_form_builder(courses):
    class ClassesFlaskForm(EditCoursesFlaskForm):
        pass

    for i, course in enumerate(courses):
        setattr(ClassesFlaskForm, f'is_monitored_course_{i}', BooleanField(label='Is monitored'))
        setattr(ClassesFlaskForm, f'auto_email_course_{i}', BooleanField(label='Auto email'))
        setattr(ClassesFlaskForm, f'short_name_course_{i}', StringField(label='Short name',
                                                                        default=course,
                                                                        render_kw={'readonly': True}))

    return ClassesFlaskForm()



