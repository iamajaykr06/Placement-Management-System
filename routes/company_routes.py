from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from routes.decorators import login_required, role_required
from models.company import (
    save_company_profile,
    get_company_profile,
    get_company_id_by_user_id
)
from models.job import create_job, get_jobs_by_company
from models.application import get_applicants_for_company_job

company_routes = Blueprint("company_routes", __name__)

@company_routes.route("/company/profile", methods=["GET", "POST"])
@login_required
@role_required("company")
def company_profile():
    user_id = session["user_id"]

    if request.method == "POST":
        try:
            save_company_profile(
                user_id=user_id,
                company_name=request.form.get("company_name", "").strip() or None,
                hr_email=request.form.get("hr_email", "").strip() or None,
                company_type=request.form.get("company_type", "").strip() or None,
                industry=request.form.get("industry", "").strip() or None,
                website=request.form.get("website", "").strip() or None,
                hr_phone=request.form.get("hr_phone", "").strip() or None,
                address=request.form.get("address", "").strip() or None,
                description=request.form.get("description", "").strip() or None,
                logo_url=request.form.get("logo_url", "").strip() or None
            )
            flash("Company profile updated successfully!", "success")
            return redirect(url_for("company_routes.company_profile"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    company = get_company_profile(user_id)
    return render_template("company_profile.html", company=company)


@company_routes.route("/company/post-job", methods=["GET", "POST"])
@login_required
@role_required("company")
def post_job():
    user_id = session["user_id"]
    company_id = get_company_id_by_user_id(user_id)

    if not company_id:
        flash("Please complete your company profile first.", "error")
        return redirect(url_for("company_routes.company_profile"))

    if request.method == "POST":
        try:
            # Get form data with defaults
            salary_min = request.form.get("salary_min")
            salary_min = float(salary_min) if salary_min else None
            
            salary_max = request.form.get("salary_max")
            salary_max = float(salary_max) if salary_max else None
            
            max_applications = request.form.get("max_applications")
            max_applications = int(max_applications) if max_applications else 100
            
            application_deadline = request.form.get("application_deadline")
            application_deadline = application_deadline if application_deadline else None
            
            create_job(
                company_id,
                request.form.get("title", "").strip(),
                request.form.get("description", "").strip(),
                request.form.get("eligibility", "").strip(),
                requirements=request.form.get("requirements", "").strip() or None,
                location=request.form.get("location", "").strip() or None,
                job_type=request.form.get("job_type", "full-time"),
                salary_min=salary_min,
                salary_max=salary_max,
                currency="INR",
                application_deadline=application_deadline,
                max_applications=max_applications
            )
            flash("Job posted successfully!", "success")
            return redirect(url_for("company_routes.post_job"))
        except ValueError as e:
            flash(f"Invalid input: {str(e)}", "error")
        except Exception as e:
            flash(f"An error occurred while posting job: {str(e)}", "error")

    try:
        jobs = get_jobs_by_company(company_id)
    except Exception as e:
        flash(f"Error loading jobs: {str(e)}", "error")
        jobs = []
    
    return render_template("post_job.html", jobs=jobs)


@company_routes.route("/company/applicants/<int:job_id>")
@login_required
@role_required("company")
def view_applicants(job_id):
    try:
        company_id = get_company_id_by_user_id(session["user_id"])
        if not company_id:
            flash("Company profile not found.", "error")
            return redirect(url_for("company_routes.company_profile"))
        
        applicants = get_applicants_for_company_job(company_id, job_id)
    except Exception as e:
        flash(f"Error loading applicants: {str(e)}", "error")
        applicants = []
    
    return render_template("company_applicants.html", applicants=applicants)


@company_routes.route("/company/dashboard")
@login_required
@role_required("company")
def company_dashboard():
    try:
        user_id = session["user_id"]
        company = get_company_profile(user_id)
        
        # Get statistics
        company_id = get_company_id_by_user_id(user_id)
        jobs = get_jobs_by_company(company_id) if company_id else []
        jobs_count = len(jobs)
        active_jobs_count = len([job for job in jobs if job.get('status') == 'active'])
        
        # Count total applicants (simplified - you might want to optimize this)
        total_applicants = 0
        for job in jobs:
            try:
                applicants = get_applicants_for_company_job(company_id, job['id'])
                total_applicants += len(applicants)
            except:
                pass
        
        return render_template("company_dashboard.html",
                             company=company,
                             jobs_count=jobs_count,
                             active_jobs_count=active_jobs_count,
                             total_applicants=total_applicants)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "error")
        return render_template("company_dashboard.html",
                             company=None,
                             jobs_count=0,
                             active_jobs_count=0,
                             total_applicants=0)
