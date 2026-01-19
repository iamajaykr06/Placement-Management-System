from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from routes.decorators import login_required, role_required

from models.student import (
    save_student_profile,
    get_student_profile,
    get_student_id_by_user_id
)

from models.application import (
    has_applied,
    apply_for_job,
    get_applications_for_student
)

from models.job import get_active_jobs, get_job_by_id

student_routes = Blueprint("student_routes", __name__)


@student_routes.route("/student/profile", methods=["GET", "POST"])
@login_required
@role_required("student")
def student_profile():
    user_id = session["user_id"]

    if request.method == "POST":
        try:
            # Get form data with defaults for optional fields
            cgpa = float(request.form.get("cgpa", 0))
            year_of_study = request.form.get("year_of_study")
            year_of_study = int(year_of_study) if year_of_study else None
            
            save_student_profile(
                user_id=user_id,
                name=request.form.get("name", "").strip() or None,
                email=request.form.get("email", "").strip() or None,
                course=request.form.get("course", "").strip() or None,
                cgpa=cgpa if cgpa > 0 else None,
                phone=request.form.get("phone", "").strip() or None,
                year_of_study=year_of_study,
                skills=request.form.get("skills", "").strip() or None,
                bio=request.form.get("bio", "").strip() or None,
                resume_url=request.form.get("resume_url", "").strip() or None,
                linkedin_url=request.form.get("linkedin_url", "").strip() or None,
                github_url=request.form.get("github_url", "").strip() or None
            )
            flash("Profile updated successfully!", "success")
            return redirect(url_for("student_routes.student_profile"))
        except ValueError as e:
            flash(f"Invalid input: {str(e)}", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    profile = get_student_profile(user_id)
    return render_template("student_profile.html", profile=profile)


@student_routes.route("/apply/<int:job_id>", methods=["GET", "POST"])
@login_required
@role_required("student")
def apply_job(job_id):
    student_id = get_student_id_by_user_id(session["user_id"])
    
    if not student_id:
        flash("Student profile not found. Please complete your profile first.", "error")
        return redirect(url_for("student_routes.student_profile"))

    if request.method == "POST":
        try:
            if has_applied(student_id, job_id):
                flash("You have already applied for this job.", "error")
                return redirect(url_for("student_routes.view_jobs"))

            apply_for_job(student_id, job_id)
            flash("Application submitted successfully!", "success")
            return redirect(url_for("student_routes.my_applications"))
        except Exception as e:
            flash(f"An error occurred while applying: {str(e)}", "error")

    job = get_job_by_id(job_id)
    if not job:
        flash("Job not found or no longer available.", "error")
        return redirect(url_for("student_routes.view_jobs"))
    
    return render_template("apply_job.html", job=job)


@student_routes.route("/jobs")
@login_required
@role_required("student")
def view_jobs():
    try:
        jobs = get_active_jobs()
    except Exception as e:
        flash(f"Error loading jobs: {str(e)}", "error")
        jobs = []
    
    return render_template("jobs.html", jobs=jobs)


@student_routes.route("/my-applications")
@login_required
@role_required("student")
def my_applications():
    try:
        student_id = get_student_id_by_user_id(session["user_id"])
        if not student_id:
            flash("Student profile not found.", "error")
            return redirect(url_for("student_routes.student_profile"))
        
        applications = get_applications_for_student(student_id)
    except Exception as e:
        flash(f"Error loading applications: {str(e)}", "error")
        applications = []
    
    return render_template("my_applications.html", applications=applications)


@student_routes.route("/student/dashboard")
@login_required
@role_required("student")
def student_dashboard():
    try:
        user_id = session["user_id"]
        profile = get_student_profile(user_id)
        
        # Get statistics
        student_id = get_student_id_by_user_id(user_id)
        applications = get_applications_for_student(student_id) if student_id else []
        applications_count = len(applications)
        pending_applications = len([app for app in applications if app.get('status') == 'pending'])
        active_jobs = len(get_active_jobs())
        
        return render_template("student_dashboard.html", 
                             profile=profile,
                             applications_count=applications_count,
                             pending_applications=pending_applications,
                             active_jobs=active_jobs)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "error")
        return render_template("student_dashboard.html", 
                             profile=None,
                             applications_count=0,
                             pending_applications=0,
                             active_jobs=0)
