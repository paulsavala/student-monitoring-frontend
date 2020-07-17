import json
import requests

from flask import render_template, current_app
from flask_login import current_user, login_required

from app.main import bp
from app.auth.decorators import registration_required
from app.utils.api import resource_url


@bp.route('/')
@login_required
@registration_required
def index():
    # Get all courses for this instructor from the LMS
    get_instructor_url = resource_url(current_app.config['API_URL'], 'get_instructor')
    api_dict = {'lms_token': current_user.lms_token}
    instructor_resp = requests.post(get_instructor_url,
                                    params={'lms': 'canvas'},
                                    data=json.dumps(api_dict)).json()
    print(instructor_resp)

    get_courses_url = resource_url(current_app.config['API_URL'], 'get_courses_by_instructor')
    course_dict = {'semester': current_app.config['SEMESTER'], 'instructor_lms_id': instructor_resp['lms_id']}
    courses_resp = requests.post(get_courses_url,
                                 params={'lms': 'canvas'},
                                 data=json.dumps(api_dict.update(course_dict))).json()
    print(courses_resp)

    # todo: Show currently registered courses and allow to add new courses from LMS/remove current courses
    return render_template('main/index.html', courses=courses_resp)


@bp.route('/about')
def about():
    return render_template('main/about.html')
