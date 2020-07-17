import requests

from flask import render_template, current_app
from flask_login import current_user, login_required

from app.main import bp
from app.auth.decorators import registration_required
from app.monitoring.forms import EditCoursesFlaskForm
from app.models import Courses
from app.utils.api import resource_url


@bp.route('/')
@login_required
@registration_required
def index():
    # Get courses which are in the db
    courses = Courses.query.filter_by(instructor_id=current_user.id).all()

    form = EditCoursesFlaskForm()
    if form.validate_on_submit():
        # If submit button was clicked
        if form.submit_changes.data:
            # Submit changes to db
            pass
        if form.refresh_courses.data:
            # If "refresh courses" button was clicked
            # Get all courses for this instructor from the LMS)
            get_courses_url = resource_url(current_app.config['API_URL'], 'get_courses_by_instructor')
            data = {'lms_token': current_user.lms_token,
                    'semester': current_app.config['SEMESTER'],
                    'instructor_lms_id': current_user.lms_id}
            courses_resp = requests.post(get_courses_url, json=data).json()

            # Check to see if they're already in the db

            # Add any that are not...

            # ...and remove any that are in the db but not returned from the LMS
    # Show the courses listed for this instructor in the db
    elif courses:
        # Recreate the form with the courses included
        courses_dict = [{'lms_id': c.lms_id,
                         'short_name': c.short_name,
                         'is_monitored': c.is_monitored,
                         'auto_email': c.auto_email} for c in courses]
        form = EditCoursesFlaskForm(courses=courses_dict)

    return render_template('main/index.html', form=form)


@bp.route('/about')
def about():
    return render_template('main/about.html')
