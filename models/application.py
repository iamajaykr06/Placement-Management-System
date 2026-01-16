from db import get_db_connection

def get_student_id_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT s.id
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE u.username = %s
        """,
        (username,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row["id"] if row else None

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

def get_job_by_id(job_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM jobs WHERE id=%s",
        (job_id,)
    )
    job = cur.fetchone()

    cur.close()
    conn.close()
    return job

def get_active_jobs():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM jobs WHERE status='active'"
    )
    jobs = cur.fetchall()

    cur.close()
    conn.close()
    return jobs

def get_applications_for_student(username):
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
        JOIN students ON applications.student_id = students.id
        JOIN users ON students.user_id = users.id
        WHERE users.username = %s
        ORDER BY applications.applied_at DESC
        """,
        (username,)
    )

    apps = cur.fetchall()
    cur.close()
    conn.close()
    return apps

def get_applicants_for_company_job(username, job_id):
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
        JOIN companies c ON j.company_id = c.id
        JOIN users cu ON c.user_id = cu.id
        WHERE a.job_id = %s
          AND cu.username = %s
        ORDER BY a.applied_at DESC
        """,
        (job_id, username)
    )

    applicants = cur.fetchall()
    cur.close()
    conn.close()
    return applicants
