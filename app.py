from flask import Flask
from routes.company_routes import company_routes
from routes.student_routes import student_routes
from routes.admin_routes import admin_routes
from routes.auth_routes import auth_routes

app = Flask(__name__)

app.secret_key="placement_secret_key"
app.register_blueprint(auth_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(student_routes)
app.register_blueprint(company_routes)
if __name__ == '__main__':
    app.run(debug=True)