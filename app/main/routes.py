import requests
import json

from flask import render_template, current_app, flash
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.auth.decorators import registration_required
from app.monitoring.forms import edit_courses_flask_form_builder, RefreshCoursesFlaskForm, DeleteAccountFlaskForm
from app.models import Courses, Instructors
from app.utils.api import resource_url


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/stedwards', methods=['GET', 'POST'])
@login_required
@registration_required
def index():
    # Get courses which are in the db
    courses = Courses.query.filter_by(instructor_id=current_user.id).order_by(Courses.short_name).all()
    # If they don't have any saved courses, just send them back
    if not courses:
        render_template('main/index.html')

    form = edit_courses_flask_form_builder([c.short_name for c in courses])

    if form.validate_on_submit():
        print('Submitting changes...')
        # Grab the values from the submitted form, compare to db, determine if we need to commit to db
        commit = False
        for c in courses:
            form_is_monitored = getattr(form, f'is_monitored_{c.short_name}').data
            form_auto_email = getattr(form, f'auto_email_{c.short_name}').data
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
        flash('Changes saved')

    # Get courses again (to reflect changes)
    courses = Courses.query.filter_by(instructor_id=current_user.id).all()
    form.num_courses = len(courses)

    # Fill in the appropriate values for monitored and auto email
    for c in courses:
        # Submit values (totally separate from display values)
        getattr(form, f'is_monitored_{c.short_name}').checked = c.is_monitored
        getattr(form, f'auto_email_{c.short_name}').checked = c.auto_email

    return render_template('main/index.html', form=form)


@bp.route('/about')
def about():
    return render_template('main/about.html')


@bp.route('/getting_started')
def getting_started():
    return render_template('main/getting_started.html')


@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    refresh_courses_form = RefreshCoursesFlaskForm()
    delete_account_form = DeleteAccountFlaskForm()
    if refresh_courses_form.validate_on_submit() and refresh_courses_form.refresh_courses.data:
        # Talk to the API to get the courses from the LMs
        print('Refresh courses')
        # Get courses from the db
        local_courses = Courses.query.filter_by(instructor_id=current_user.id).all()
        # Get all courses for this instructor from the LMS
        get_courses_url = resource_url(current_app.config['API_URL'], 'get_courses_by_instructor')
        data = {'lms_token': current_user.lms_token,
                'semester': current_app.config['SEMESTER'],
                'instructor_lms_id': current_user.lms_id}
        courses_resp = requests.post(get_courses_url, json=json.dumps(data)).json()

        # Check to see if they're already in the db
        db_course_lms_ids = set([str(c.lms_id) for c in local_courses])
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
        flash('Courses updated')

    if delete_account_form.validate_on_submit() and delete_account_form.delete_account.data:
        Courses.query.filter_by(instructor_id=current_user.id).delete()
        Instructors.query.filter_by(id=current_user.id).delete()
        db.session.commit()
        print(f'Deleting account for user {current_user.id}')
        flash('Your account has been deleted')
        return render_template('main/about.html')

    return render_template('main/settings.html',
                           refresh_courses_form=refresh_courses_form,
                           delete_account_form=delete_account_form)
