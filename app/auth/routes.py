from app import db
from app.auth.forms import RegisterForm
from app.models import Instructor
from app.models import Department
from app.main import bp
from app.auth.google_login import google_login_request_uri, process_google_login_callback

from flask import render_template, redirect, flash, url_for, current_app
from flask_login import login_required, login_user, logout_user, current_user
from flask_babel import _


@bp.route('/login')
def login():
    request_uri = google_login_request_uri()
    return redirect(request_uri)


@bp.route('/login/callback')
def callback():
    callback_result = process_google_login_callback()
    if callback is None:
        flash('Verify your Google email address before proceeding')
        return redirect(url_for('about'))

    user_id = callback_result['user_id']
    email = callback_result['email']

    # Check if instructor already exists in the db. If not, save to db redirect to complete registration.
    instructor = Instructor.query.filter(id=user_id).first()
    if instructor is None:
        if instructor.email in current_app.config.ADMINS:
            is_admin = True
        else:
            is_admin = False
        instructor = Instructor(id=user_id, email=email, registered=False, is_admin=is_admin)
        db.session.add(instructor)
        db.session.commit()
        login_user(instructor)
        return redirect(url_for('register'))

    # Login user
    login_user(instructor)
    flash(_('You are now logged in'))

    # Send back to homepage
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        instructor = Instructor.query.filter(id=current_user.id).one()
    except Exception as e:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    # If they just submitted the form, then update and save their data
    if form.validate_on_submit():
        # Fill in remaining data and save to db
        instructor.first_name = form.first_name.data
        instructor.last_name = form.last_name.data
        instructor.department_id = form.department.data
        instructor.api_token = form.api_token.data
        instructor.registered = True

        db.session.add(instructor)
        db.session.commit()

        return redirect(url_for('index'))
    # Otherwise, ask for the remaining info
    else:
        # Set the departments from the db
        departments = Department.query.all()
        form.department.choices = [(row.id, row.long_name) for row in departments]
        return render_template('forms/register.html', form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
