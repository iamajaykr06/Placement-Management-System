from db import get_db_connection

# -------------------- STUDENT SIDE --------------------

def has_applied(student_id, job_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM applications WHERE student_id=%s AND job_id=%s",
        (student_id, job_id)
    )

    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists


def apply_for_job(student_id, job_id, cover_letter=None):
    """
    Apply for a job. Optionally include a cover letter.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO applications (student_id, job_id, cover_letter) VALUES (%s, %s, %s)",
        (student_id, job_id, cover_letter)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_applications_for_student(student_id):
    """
    Get all applications for a student with job and company details.
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT 
            applications.id AS application_id,
            jobs.id AS job_id,
            jobs.title AS job_title,
            jobs.location,
            jobs.job_type,
            companies.company_name,
            companies.id AS company_id,
            applications.status,
            applications.applied_at,
            applications.reviewed_at,
            applications.cover_letter
        FROM applications
        JOIN jobs ON applications.job_id = jobs.id
        JOIN companies ON jobs.company_id = companies.id
        WHERE applications.student_id = %s
        ORDER BY applications.applied_at DESC
        """,
        (student_id,)
    )

    apps = cur.fetchall()
    cur.close()
    conn.close()
    return apps


# -------------------- COMPANY SIDE --------------------

def get_applicants_for_company_job(company_id, job_id):
    """
    Get all applicants for a specific job posting with student details.
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT 
            a.id AS application_id,
            s.id AS student_id,
            s.name AS student_name,
            s.course,
            s.cgpa,
            s.skills,
            s.resume_url,
            s.linkedin_url,
            s.github_url,
            u.email AS student_email,
            a.status,
            a.applied_at,
            a.reviewed_at,
            a.cover_letter,
            a.notes
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN users u ON s.user_id = u.id
        JOIN jobs j ON a.job_id = j.id
        WHERE j.company_id = %s
          AND a.job_id = %s
        ORDER BY a.applied_at DESC
        """,
        (company_id, job_id)
    )

    applicants = cur.fetchall()
    cur.close()
    conn.close()
    return applicants

def update_application_status(application_id, status, notes=None):
    """
    Update the status of an application (for companies to manage applications).
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    if notes:
        cur.execute(
            """
            UPDATE applications 
            SET status = %s, reviewed_at = CURRENT_TIMESTAMP, notes = %s
            WHERE id = %s
            """,
            (status, notes, application_id)
        )
    else:
        cur.execute(
            """
            UPDATE applications 
            SET status = %s, reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (status, application_id)
        )
    
    conn.commit()
    cur.close()
    conn.close()

def get_application_by_id(application_id):
    """
    Get a specific application by ID.
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    cur.execute(
        """
        SELECT a.*, 
               s.name AS student_name,
               s.email AS student_email,
               s.course,
               s.cgpa,
               j.title AS job_title,
               c.company_name
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN jobs j ON a.job_id = j.id
        JOIN companies c ON j.company_id = c.id
        WHERE a.id = %s
        """,
        (application_id,)
    )
    
    application = cur.fetchone()
    cur.close()
    conn.close()
    return application
