from flask import redirect, url_for, request, render_template
from functools import wraps

from flask_login import current_user, logout_user


def login_required_user(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login", next=request.url))

        return f(*args, **kwargs)

    return check
