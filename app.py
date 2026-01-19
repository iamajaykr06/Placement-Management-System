from flask import Flask, redirect, url_for, session, render_template
from routes.company_routes import company_routes
from routes.student_routes import student_routes
from routes.admin_routes import admin_routes
from routes.auth_routes import auth_routes

app = Flask(__name__)

app.secret_key = "placement_secret_key"

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(student_routes)
app.register_blueprint(company_routes)

# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        role = session.get('role', '').lower()
        if role == 'admin':
            return redirect(url_for('admin_routes.admin_dashboard'))
        elif role == 'company':
            return redirect(url_for('company_routes.company_dashboard'))
        elif role == 'student':
            return redirect(url_for('student_routes.student_dashboard'))
    # Show landing page for visitors
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)