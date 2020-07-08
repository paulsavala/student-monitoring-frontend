from functools import wraps
from flask import request, redirect, url_for
from flask_login import current_user


def registration_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_registered:
            return redirect(url_for('auth.register', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
