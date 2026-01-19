from functools import wraps
from flask import session, redirect, url_for, flash
from models.user import get_user_by_id

def login_required(fn):
    """
    Decorator to ensure user is logged in.
    Redirects to login page if not authenticated.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login to access this page.", "error")
            return redirect(url_for("auth_routes.login"))
        
        # Optional: Check if user is still active
        try:
            user = get_user_by_id(session["user_id"])
            if user and not user.get("is_active", True):
                session.clear()
                flash("Your account has been deactivated. Please contact administrator.", "error")
                return redirect(url_for("auth_routes.login"))
        except:
            pass  # If user check fails, continue anyway
        
        return fn(*args, **kwargs)
    return wrapper


def role_required(role):
    """
    Decorator to ensure user has the required role.
    Redirects to login page if role doesn't match.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login to access this page.", "error")
                return redirect(url_for("auth_routes.login"))
            
            if "role" not in session:
                flash("Invalid session. Please login again.", "error")
                session.clear()
                return redirect(url_for("auth_routes.login"))

            if session["role"].lower() != role.lower():
                flash(f"Access denied. This page is only for {role}s.", "error")
                return redirect(url_for("auth_routes.login"))

            return fn(*args, **kwargs)
        return wrapper
    return decorator
