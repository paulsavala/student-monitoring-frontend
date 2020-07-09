from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user
from flask_babel import _


def registration_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_registered:
            flash(_('Please complete registration before continuing'))
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
