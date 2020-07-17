import json
import requests

from flask import render_template, current_app
from flask_login import current_user, login_required

from app.main import bp
from app.auth.decorators import registration_required
from app.utils.api import resource_url
from app.models import CourseInstances


@bp.route('/')
@login_required
@registration_required
def index():
    # Get all courses for this instructor from the LMS)
    get_courses_url = resource_url(current_app.config['API_URL'], 'get_courses_by_instructor')
    data = {'lms_token': current_user.lms_token,
            'semester': current_app.config['SEMESTER'],
            'instructor_lms_id': current_user.lms_id}
    print(data)
    courses_resp = requests.post(get_courses_url,
                                 json=data).json()
    print(courses_resp)

    # Get courses which are currently being monitored
    active_courses = CourseInstances.query.filter_by(instructor_id=current_user.id).all()
    if active_courses:
        print(active_courses)

    # todo: Show currently registered courses and allow to add new courses from LMS/remove current courses
    return render_template('main/index.html', courses=courses_resp)


@bp.route('/about')
def about():
    return render_template('main/about.html')
