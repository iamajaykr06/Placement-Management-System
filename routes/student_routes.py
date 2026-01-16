from flask import Blueprint, render_template, session, request
from models.student import (get_user_id_by_username,
                            save_student_profile,
                            get_student_profile)

from routes.decorators import login_required, role_required
from models.application import (get_student_id_by_username,
                                has_applied,
                                apply_for_job,
                                get_job_by_id,
                                get_active_jobs,
                                get_applications_for_student
                                )
student_routes = Blueprint("student_routes", __name__)

@student_routes.route("/student/profile", methods=["GET", "POST"])
@login_required
@role_required("student")
def student_profile():

    user_id = get_user_id_by_username(session["user"])

    if request.method == "POST":
        save_student_profile(
            user_id=user_id,
            name=request.form["name"],
            email=request.form["email"],
            course=request.form["course"],
            cgpa=request.form["cgpa"]
        )

    profile = get_student_profile(user_id)

    return render_template("student_profile.html", profile=profile)

@student_routes.route("/apply/<int:job_id>", methods=["GET", "POST"])
@login_required
@role_required("student")
def apply_job(job_id):

    student_id = get_student_id_by_username(session["user"])

    if request.method == "POST":
        if has_applied(student_id, job_id):
            return "You have already applied for this job."

        apply_for_job(student_id, job_id)
        return "Application submitted successfully."

    job = get_job_by_id(job_id)
    return render_template("apply_job.html", job=job)

@student_routes.route("/jobs")
@login_required
@role_required("student")
def view_jobs():
    jobs = get_active_jobs()
    return render_template("jobs.html", jobs=jobs)

@student_routes.route("/my-applications")
@login_required
@role_required("student")
def my_applications():
    applications = get_applications_for_student(session["user"])
    return render_template(
        "my_applications.html",
        applications=applications
    )

@student_routes.route("/student/dashboard")
@login_required
@role_required("student")
def student_dashboard():
    return render_template("student_dashboard.html")
