from flask import Blueprint, render_template, flash
from routes.decorators import login_required, role_required
from db import get_db_connection

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route("/admin")
@login_required
@role_required("admin")
def admin_dashboard():
    """
    Admin dashboard with system statistics.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get total students
        cursor.execute("SELECT COUNT(*) as count FROM students")
        total_students = cursor.fetchone()['count']
        
        # Get total companies
        cursor.execute("SELECT COUNT(*) as count FROM companies")
        total_companies = cursor.fetchone()['count']
        
        # Get total jobs
        cursor.execute("SELECT COUNT(*) as count FROM jobs")
        total_jobs = cursor.fetchone()['count']
        
        # Get active jobs
        cursor.execute("SELECT COUNT(*) as count FROM jobs WHERE status = 'active'")
        active_jobs = cursor.fetchone()['count']
        
        # Get total applications
        cursor.execute("SELECT COUNT(*) as count FROM applications")
        total_applications = cursor.fetchone()['count']
        
        # Get pending applications
        cursor.execute("SELECT COUNT(*) as count FROM applications WHERE status = 'pending'")
        pending_applications = cursor.fetchone()['count']
        
        # Get accepted applications
        cursor.execute("SELECT COUNT(*) as count FROM applications WHERE status = 'accepted'")
        accepted_applications = cursor.fetchone()['count']
        
        # Get total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()['count']
        
        # Get active users
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_active = TRUE")
        active_users = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return render_template("admin_dashboard.html",
                             total_students=total_students,
                             total_companies=total_companies,
                             total_jobs=total_jobs,
                             active_jobs=active_jobs,
                             total_applications=total_applications,
                             pending_applications=pending_applications,
                             accepted_applications=accepted_applications,
                             total_users=total_users,
                             active_users=active_users)
    except Exception as e:
        flash(f"Error loading dashboard statistics: {str(e)}", "error")
        return render_template("admin_dashboard.html",
                             total_students=0,
                             total_companies=0,
                             total_jobs=0,
                             active_jobs=0,
                             total_applications=0,
                             pending_applications=0,
                             accepted_applications=0,
                             total_users=0,
                             active_users=0)
