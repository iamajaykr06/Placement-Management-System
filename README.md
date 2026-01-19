# Placement Management System

A comprehensive Flask-based web application for managing placement activities, connecting students with companies for job opportunities.

## 🚀 Features

### For Students
- ✅ Complete profile management (skills, bio, social links)
- ✅ Browse available job opportunities
- ✅ One-click job application
- ✅ Track application status
- ✅ View application history
- ✅ Modern, responsive dashboard

### For Companies
- ✅ Detailed company profile
- ✅ Post comprehensive job listings
- ✅ Set salary ranges and deadlines
- ✅ View and manage applicants
- ✅ Track job performance (views, applications)
- ✅ Company dashboard with statistics

### System Features
- ✅ User authentication and authorization
- ✅ Role-based access control (Student, Company, Admin)
- ✅ Beautiful landing page
- ✅ Modern UI/UX design
- ✅ Responsive design (mobile-friendly)
- ✅ Flash messages for user feedback
- ✅ Database optimization with indexes
- ✅ Error handling and validation

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🛠️ Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Placement-Management-System
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

Update `db.py` with your MySQL credentials:
```python
host="localhost"
user="your_username"
password="your_password"
database="placement_db"
```

### Step 5: Set Up Database

**Option A: Fresh Installation**
```bash
mysql -u root -p < database_schema_improved.sql
```

**Option B: Migration from Existing Database**
```bash
# 1. Backup your database first!
mysqldump -u root -p placement_db > backup.sql

# 2. Run migration script
python migrate_database.py
```

## 🏃 Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📁 Project Structure

```
Placement-Management-System/
├── app.py                          # Main Flask application
├── db.py                           # Database connection
├── migrate_database.py             # Database migration script
├── requirements.txt                 # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── auth/                           # Authentication module
│   ├── __init__.py
│   └── auth.py                    # Password hashing utilities
│
├── models/                         # Database models
│   ├── __init__.py
│   ├── user.py                    # User model
│   ├── student.py                 # Student model
│   ├── company.py                 # Company model
│   ├── job.py                     # Job model
│   └── application.py             # Application model
│
├── routes/                         # Flask routes/blueprints
│   ├── __init__.py
│   ├── auth_routes.py             # Authentication routes
│   ├── student_routes.py          # Student routes
│   ├── company_routes.py          # Company routes
│   ├── admin_routes.py            # Admin routes
│   └── decorators.py              # Route decorators
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Landing page
│   ├── login.html                 # Login page
│   ├── register_student.html      # Student registration
│   ├── register_company.html      # Company registration
│   ├── student_dashboard.html     # Student dashboard
│   ├── student_profile.html       # Student profile
│   ├── jobs.html                  # Job listings
│   ├── apply_job.html             # Apply for job
│   ├── my_applications.html       # Student applications
│   ├── company_dashboard.html     # Company dashboard
│   ├── company_profile.html       # Company profile
│   ├── post_job.html              # Post job
│   ├── company_applicants.html    # View applicants
│   └── admin_dashboard.html       # Admin dashboard
│
├── static/                         # Static files
│   └── style.css                  # Modern CSS styles
│
├── database_schema_improved.sql    # Improved database schema
├── DATABASE_IMPROVEMENTS.md       # Database improvements guide
└── PROJECT_SUMMARY.md             # Project summary
```

## 🎯 Usage

### For Students

1. **Register**: Go to `/register/student` and create an account
2. **Complete Profile**: Add your details, skills, and professional links
3. **Browse Jobs**: Visit `/jobs` to see available opportunities
4. **Apply**: Click on any job to view details and apply
5. **Track**: Check `/my-applications` to see your application status

### For Companies

1. **Register**: Go to `/register/company` and create an account
2. **Complete Profile**: Add company information and details
3. **Post Jobs**: Visit `/company/post-job` to create job listings
4. **Manage**: View applicants for each job posting
5. **Track**: Monitor job performance on your dashboard

## 🔧 Configuration

### Database Configuration
Edit `db.py` to set your MySQL connection details.

### Secret Key
For production, change the secret key in `app.py`:
```python
app.secret_key = "your-secret-key-here"
```

Or use environment variables:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
```

## 📊 Database Schema

The application uses the following main tables:
- `users` - User authentication and roles
- `students` - Student profiles
- `companies` - Company profiles
- `jobs` - Job postings
- `applications` - Job applications
- `notifications` - User notifications (optional)
- `activity_logs` - Audit trail (optional)

See `database_schema_improved.sql` for complete schema details.

## 🔒 Security Notes

⚠️ **Before deploying to production:**

1. Change the secret key in `app.py`
2. Use environment variables for database credentials
3. Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
4. Use HTTPS in production
5. Implement proper input validation
6. Add CSRF protection
7. Regularly update dependencies
8. Set up database backups

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure MySQL server is running
- Verify credentials in `db.py`
- Check if database exists: `mysql -u root -p -e "SHOW DATABASES;"`
- Run `python migrate_database.py` to verify connection

### Import Errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Port Already in Use
- Change port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000

## 📚 Documentation

- `DATABASE_IMPROVEMENTS.md` - Complete database improvements guide
- `PROJECT_SUMMARY.md` - Project overview and features
- `database_schema_improved.sql` - Full database schema

## 🚀 Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ for better placements**
