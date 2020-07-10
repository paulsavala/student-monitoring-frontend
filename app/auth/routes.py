from app import db
from app.auth.forms import RegisterFlaskForm
from app.models import Instructors
from app.models import Departments
from app.auth import bp
from app.auth.google_login import google_login_request_uri, process_google_login_callback

from flask import render_template, redirect, flash, url_for, current_app
from flask_login import login_required, login_user, logout_user, current_user
from flask_babel import _


@bp.route('/login', methods=['GET', 'POST'])
def login():
    request_uri = google_login_request_uri()
    return redirect(request_uri)


@bp.route('/login/callback')
def callback():
    callback_result = process_google_login_callback()
    if callback is None:
        flash(_('Verify your Google email address before proceeding'))
        return redirect(url_for('main.about'))

    email = callback_result['email']

    # Check if instructor already exists in the db. If not, save to db redirect to complete registration.
    instructor = Instructors.query.filter_by(email=email).first()
    if instructor is None:
        if email in current_app.config['ADMINS']:
            is_admin = True
        else:
            is_admin = False
        instructor = Instructors(email=email,
                                 is_registered=False,
                                 is_admin=is_admin,
                                 school_id=current_app.config['SCHOOL_ID'])
        db.session.add(instructor)
        db.session.commit()

        # Grab the user from the db so that it can be logged in
        instructor = Instructors.query.filter_by(email=email).one()
        login_user(instructor)

        return redirect(url_for('auth.register'))
    else:
        login_user(instructor)
        return redirect(url_for('main.index'))


@login_required
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFlaskForm()
    # Set the departments from the db
    # Note that this must occur before form.validate_on_submit, otherwise validation will fail for empty choices
    departments = Departments.query.all()
    form.department.choices = [(row.id, row.long_name) for row in departments]
    # If they just submitted the form, then update and save their data
    if form.validate_on_submit():
        # Fill in remaining data and save to db
        instructor = Instructors.query.filter_by(email=current_user.email).one()

        print(form.department.data)
        instructor.first_name = form.first_name.data
        instructor.last_name = form.last_name.data
        instructor.department_id = form.department.data
        instructor.api_token = form.api_token.data
        instructor.is_registered = True

        db.session.commit()

        return redirect(url_for('main.index'))
    # Otherwise, ask for the remaining info
    else:
        return render_template('auth/register.html', form=form)


@login_required
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
