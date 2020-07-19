import requests

from flask import render_template, current_app
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.auth.decorators import registration_required
from app.monitoring.forms import edit_courses_flask_form_builder
from app.models import Courses
from app.utils.api import resource_url


@bp.route('/', methods=['GET', 'POST'])
@login_required
@registration_required
def index():
    # Get courses which are in the db
    courses = Courses.query.filter_by(instructor_id=current_user.id).all()
    # If they don't have any saved courses, just send them back
    if not courses:
        render_template('main/index.html')

    form = edit_courses_flask_form_builder([c.short_name for c in courses])

    if form.validate_on_submit():
        # If submit button was clicked
        if form.submit_changes.data:
            print('Submitting changes...')
            # Grab the values from the submitted form, compare to db, determine if we need to commit to db
            commit = False
            for i, c in enumerate(courses):
                form_is_monitored = getattr(form, f'is_monitored_{i}').data
                form_auto_email = getattr(form, f'auto_email_{i}').data
                if form_is_monitored != c.is_monitored:
                    c.is_monitored = form_is_monitored
                    commit = True
                    print(f'Changing course {c.short_name} to is_monitored={form_is_monitored}')
                if form_auto_email != c.auto_email:
                    c.auto_email = form_auto_email
                    commit = True
                    print(f'Changing course {c.short_name} to auto_email={form_auto_email}')
            if commit:
                print('Commiting submissions to db...')
                db.session.commit()
        # Get courses again (to reflect changes)
        courses = Courses.query.filter_by(instructor_id=current_user.id).all()
        form.num_courses = len(courses)
        # If the refresh button courses was clicked, talk to the API to get the courses from the LMs
        if form.refresh_courses.data:
            print('Refresh courses')
            # Get all courses for this instructor from the LMS
            get_courses_url = resource_url(current_app.config['API_URL'], 'get_courses_by_instructor')
            data = {'lms_token': current_user.lms_token,
                    'semester': current_app.config['SEMESTER'],
                    'instructor_lms_id': current_user.lms_id}
            courses_resp = requests.post(get_courses_url, json=data).json()

            # Check to see if they're already in the db
            db_course_lms_ids = set([str(c.lms_id) for c in courses])
            lms_course_lms_ids = set([str(c['lms_id']) for c in courses_resp])

            new_course_ids = lms_course_lms_ids - db_course_lms_ids
            new_courses = [c for c in courses_resp if c['lms_id'] in new_course_ids]
            old_course_ids = db_course_lms_ids - lms_course_lms_ids
            old_courses = [c for c in courses_resp if c['lms_id'] in old_course_ids]

            # Add any that are not...
            courses_to_add = ([Courses(lms_id=c['lms_id'],
                                       season=current_app.config['SEASON'],
                                       year=current_app.config['YEAR'],
                                       short_name=c['short_name'],
                                       long_name=c['long_name'],
                                       is_monitored=False,
                                       auto_email=False,
                                       instructor_id=current_user.id) for c in new_courses])
            print(f'Adding to db: {[c.short_name for c in courses_to_add]}')
            for c in courses_to_add:
                db.session.add(c)

            # ...and remove any that are in the db but not returned from the LMS
            courses_to_remove = ([Courses.query.filter_by(id=c.id) for c in old_courses])
            print(f'Deleting from db: {[c.short_name for c in courses_to_remove]}')
            for c in courses_to_remove:
                db.session.remove(c)

            # Get courses again (to reflect changes)
            courses = Courses.query.filter_by(instructor_id=current_user.id).all()
            form.num_courses = len(courses)

    # Fill in the appropriate values for monitored and auto email
    for i, c in enumerate(courses):
        getattr(form, f'is_monitored_{i}').default = c.is_monitored
        getattr(form, f'auto_email_{i}').default = c.auto_email

    return render_template('main/index.html', form=form)


@bp.route('/about')
def about():
    return render_template('main/about.html')
