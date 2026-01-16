from flask import Blueprint,render_template

from routes.decorators import login_required, role_required

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route("/admin")
@login_required
@role_required("admin")
def admin_panel():
    return "Admin Panel"

@admin_routes.route("/admin")
@login_required
@role_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")
