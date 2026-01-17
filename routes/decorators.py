from functools import wraps
from flask import session, redirect, url_for

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth_routes.login"))
        return fn(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "role" not in session:
                return redirect(url_for("auth_routes.login"))

            if session["role"] != role:
                return redirect(url_for("auth_routes.login"))

            return fn(*args, **kwargs)
        return wrapper
    return decorator
