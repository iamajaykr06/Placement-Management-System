from flask import Blueprint, session, render_template, redirect, request, url_for
from models.student import save_student_profile
from auth.auth import verify_password
from models.company import save_company_profile
from models.user import get_user_by_email, register_user

auth_routes = Blueprint("auth_routes", __name__)

# -------------------- STUDENT REGISTRATION --------------------

@auth_routes.route("/register/student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        try:
            user_id = register_user(
                username=request.form["username"].strip(),
                email=request.form["email"].strip(),
                password=request.form["password"],
                role="student"
            )
        except ValueError:
            return "User already exists", 400

        # 🔥 CREATE STUDENT PROFILE IMMEDIATELY
        save_student_profile(
            user_id=user_id,
            name="",        # empty initially
            email=request.form["email"].strip(),
            course="",
            cgpa=0.0
        )

        return redirect(url_for("auth_routes.login"))

    return render_template("register_student.html")


# -------------------- COMPANY REGISTRATION --------------------

@auth_routes.route("/register/company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        try:
            user_id = register_user(
                username=request.form["username"].strip(),
                email=request.form["email"].strip(),
                password=request.form["password"],
                role="company"
            )
        except ValueError:
            return "User already exists", 400

        save_company_profile(
            user_id,
            request.form["company_name"].strip(),
            request.form["hr_email"].strip()
        )

        return redirect(url_for("auth_routes.login"))

    return render_template("register_company.html")

# -------------------- LOGIN --------------------

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        user = get_user_by_email(email)
        if not user or not verify_password(password, user["password"]):
            return "Invalid credentials", 401

        role = user["role"].strip().lower()
        session["user_id"] = user["id"]
        session["role"] = role

        if role == "admin":
            return redirect(url_for("admin_routes.admin_dashboard"))
        elif role == "company":
            return redirect(url_for("company_routes.company_dashboard"))
        elif role == "student":
            return redirect(url_for("student_routes.student_dashboard"))
        else:
            return "Invalid role", 403

    return render_template("login.html")


# -------------------- LOGOUT --------------------

@auth_routes.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_routes.login"))
