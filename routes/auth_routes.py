from flask import Blueprint, session, render_template, redirect, request, url_for, flash
from models.student import save_student_profile
from auth.auth import (
    verify_password,
    validate_password_strength_medium,
    validate_email,
    validate_username,
    sanitize_input
)
from models.company import save_company_profile
from models.user import get_user_by_email, register_user

auth_routes = Blueprint("auth_routes", __name__)

# -------------------- STUDENT REGISTRATION --------------------

@auth_routes.route("/register/student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        try:
            # Validate and sanitize inputs
            username = sanitize_input(request.form.get("username", "").strip(), max_length=30)
            email = sanitize_input(request.form.get("email", "").strip(), max_length=255)
            password = request.form.get("password", "")
            
            # Validate username
            username_valid, username_msg = validate_username(username)
            if not username_valid:
                flash(username_msg, "error")
                return render_template("register_student.html")
            
            # Validate email
            if not validate_email(email):
                flash("Please enter a valid email address.", "error")
                return render_template("register_student.html")
            
            # Validate password strength
            password_valid, password_msg = validate_password_strength_medium(password)
            if not password_valid:
                flash(password_msg, "error")
                return render_template("register_student.html")
            
            user_id = register_user(
                username=username,
                email=email,
                password=password,
                role="student"
            )
            
            # CREATE STUDENT PROFILE IMMEDIATELY
            save_student_profile(
                user_id=user_id,
                name=None,        # empty initially
                email=email,
                course=None,
                cgpa=None
            )
            
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth_routes.login"))
            
        except ValueError:
            flash("Email or username already exists. Please try again.", "error")
        except Exception as e:
            flash(f"An error occurred during registration: {str(e)}", "error")

    return render_template("register_student.html")


# -------------------- COMPANY REGISTRATION --------------------

@auth_routes.route("/register/company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        try:
            # Validate and sanitize inputs
            username = sanitize_input(request.form.get("username", "").strip(), max_length=30)
            email = sanitize_input(request.form.get("email", "").strip(), max_length=255)
            password = request.form.get("password", "")
            company_name = sanitize_input(request.form.get("company_name", "").strip(), max_length=255)
            hr_email = sanitize_input(request.form.get("hr_email", "").strip(), max_length=255)
            
            # Validate username
            username_valid, username_msg = validate_username(username)
            if not username_valid:
                flash(username_msg, "error")
                return render_template("register_company.html")
            
            # Validate email
            if not validate_email(email):
                flash("Please enter a valid email address.", "error")
                return render_template("register_company.html")
            
            # Validate HR email
            if not validate_email(hr_email):
                flash("Please enter a valid HR email address.", "error")
                return render_template("register_company.html")
            
            # Validate password strength
            password_valid, password_msg = validate_password_strength_medium(password)
            if not password_valid:
                flash(password_msg, "error")
                return render_template("register_company.html")
            
            # Validate company name
            if not company_name or len(company_name) < 2:
                flash("Company name must be at least 2 characters long.", "error")
                return render_template("register_company.html")
            
            user_id = register_user(
                username=username,
                email=email,
                password=password,
                role="company"
            )
            
            save_company_profile(
                user_id=user_id,
                company_name=company_name,
                hr_email=hr_email
            )
            
            flash("Company registration successful! Please login.", "success")
            return redirect(url_for("auth_routes.login"))
            
        except ValueError:
            flash("Email or username already exists. Please try again.", "error")
        except Exception as e:
            flash(f"An error occurred during registration: {str(e)}", "error")

    return render_template("register_company.html")

# -------------------- LOGIN --------------------

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Sanitize inputs
        email = sanitize_input(request.form.get("email", "").strip(), max_length=255)
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("login.html")
        
        # Validate email format
        if not validate_email(email):
            flash("Please enter a valid email address.", "error")
            return render_template("login.html")

        user = get_user_by_email(email)
        if not user:
            flash("Invalid email or password. Please try again.", "error")
            return render_template("login.html")
        
        # Check if user is active
        if not user.get("is_active", True):
            flash("Your account has been deactivated. Please contact administrator.", "error")
            return render_template("login.html")
        
        if not verify_password(password, user["password"]):
            flash("Invalid email or password. Please try again.", "error")
            return render_template("login.html")

        # Update last login timestamp
        try:
            from db import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                (user["id"],)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except:
            pass  # If update fails, continue anyway

        role = user["role"].strip().lower()
        session["user_id"] = user["id"]
        session["role"] = role

        flash(f"Welcome back! Logged in as {role}.", "success")
        
        if role == "admin":
            return redirect(url_for("admin_routes.admin_dashboard"))
        elif role == "company":
            return redirect(url_for("company_routes.company_dashboard"))
        elif role == "student":
            return redirect(url_for("student_routes.student_dashboard"))
        else:
            flash("Invalid user role.", "error")
            session.clear()
            return render_template("login.html")

    return render_template("login.html")


# -------------------- LOGOUT --------------------

@auth_routes.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth_routes.login"))
