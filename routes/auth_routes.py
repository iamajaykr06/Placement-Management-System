from flask import Blueprint, session, render_template, redirect, request, url_for

from auth.auth import hash_password, verify_password
from models.user import get_user_by_username, create_user

auth_routes=Blueprint('auth_routes',__name__)

@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        if get_user_by_username(username):
            return "User already exists"

        user_id = create_user(
            username,
            email,
            hash_password(password),
            role
        )

        return redirect(url_for("auth_routes.login"))

    return render_template("register.html")

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)
        if not user or not verify_password(password, user["password"]):
            return "Invalid credentials"

        # set session
        session["user"] = user["username"]
        session["role"] = user["role"]

        # 🔑 ROLE-BASED REDIRECT (HERE)
        if user["role"] == "admin":
            return redirect("/admin")
        elif user["role"] == "company":
            return redirect("/company/dashboard")
        else:
            return redirect("/student/dashboard")

    return render_template("login.html")

@auth_routes.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth_routes.login"))