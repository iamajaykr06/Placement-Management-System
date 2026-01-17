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


def apply_for_job(student_id, job_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO applications (student_id, job_id) VALUES (%s, %s)",
        (student_id, job_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_applications_for_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT 
            jobs.title AS job_title,
            companies.company_name,
            applications.status,
            applications.applied_at
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
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT 
            s.name AS student_name,
            u.email AS student_email,
            a.status,
            a.applied_at
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
