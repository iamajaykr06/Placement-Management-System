from flask import Blueprint,render_template,request,session,redirect,url_for
from models.company import (get_user_id_by_username,
                            save_company_profile,
                            get_company_profile)
from routes.decorators import login_required, role_required

from models.job import (get_company_id_by_username,
                        create_job,
                        get_jobs_by_company
                        )

from models.application import get_applicants_for_company_job

company_routes = Blueprint('company_routes',__name__)

@company_routes.route('/company/profile',methods=['GET'])
@login_required
@role_required(role='Company')
def company_profile():
    user_id=get_user_id_by_username(session['user'])

    if request.method == 'POST':
        save_company_profile(
            user_id=user_id,
             company_name=request.form['company_name'],
              hr_email=request.form['hr_email']
        )
    company = get_company_profile(user_id)
    return render_template("company_profile.html",company=company)

@company_routes.route("/company/post-job", methods=["GET", "POST"])
@login_required
@role_required("company")
def post_job():

    company_id = get_company_id_by_username(session["user"])
    if not company_id:
        return redirect(url_for("company_routes.company_profile"))

    if request.method == "POST":
        create_job(
            company_id,
            request.form["title"],
            request.form["description"],
            request.form["eligibility"]
        )

    jobs = get_jobs_by_company(company_id)
    return render_template("post_job.html", jobs=jobs)

@company_routes.route("/company/applicants/<int:job_id>")
@login_required
@role_required("company")
def view_applicants(job_id):
    applicants = get_applicants_for_company_job(
        session["user"],
        job_id
    )
    return render_template(
        "company_applicants.html",
        applicants=applicants
    )

@company_routes.route("/company/dashboard")
@login_required
@role_required("company")
def company_dashboard():
    return render_template("company_dashboard.html")
