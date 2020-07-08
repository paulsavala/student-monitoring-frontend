import json
import requests

from flask import render_template, current_app
from flask_login import current_user, login_required

from app.main import bp
from app.auth.decorators import registration_required


@login_required
@registration_required
@bp.route('/')
def index():
    # Get all courses for this instructor from the LMS
    get_instructor_url = current_app.config.api_url + '/get_instructor'
    api_dict = {'api_url': current_app.config.lms_url, 'api_token': current_user.api_token}
    instructor_resp = requests.post(get_instructor_url,
                                    params={'lms': 'canvas'},
                                    data=json.dumps(api_dict)).json()

    get_courses_url = current_app.config.api_url + '/get_courses_by_instructor'
    course_dict = {'semester': current_app.config.semester, 'instructor_lms_id': instructor_resp['lms_id']}
    courses_resp = requests.post(get_courses_url,
                                 params={'lms': 'canvas'},
                                 data=json.dumps(api_dict.update(course_dict)).json())

    # todo: Show currently registered courses and allow to add new courses from LMS/remove current courses
    return render_template('pages/home.html')


@bp.route('/about')
def about():
    return render_template('pages/about.html')