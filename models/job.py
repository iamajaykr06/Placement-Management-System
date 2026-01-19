from db import get_db_connection

def create_job(company_id, title, description, eligibility, requirements=None,
               location=None, job_type='full-time', salary_min=None, salary_max=None,
               currency='INR', application_deadline=None, max_applications=100):
    """
    Create a new job posting with all available fields.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO jobs (company_id, title, description, eligibility, requirements,
                         location, job_type, salary_min, salary_max, currency,
                         application_deadline, max_applications)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (company_id, title, description, eligibility, requirements,
         location, job_type, salary_min, salary_max, currency,
         application_deadline, max_applications)
    )
    conn.commit()

    cur.close()
    conn.close()

def increment_job_views(job_id):
    """Increment view count for a job"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE jobs SET views_count = views_count + 1 WHERE id = %s",
        (job_id,)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_jobs_by_company(company_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM jobs WHERE company_id=%s",
        (company_id,)
    )
    jobs = cur.fetchall()

    cur.close()
    conn.close()
    return jobs

def get_active_jobs():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT j.*, c.company_name 
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.id
        WHERE j.status = 'active'
        ORDER BY j.created_at DESC
        """
    )

    jobs = cur.fetchall()
    cur.close()
    conn.close()
    return jobs

def get_job_by_id(job_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT j.*, c.company_name, c.industry, c.logo_url
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.id
        WHERE j.id = %s
        """,
        (job_id,)
    )

    job = cur.fetchone()
    cur.close()
    conn.close()
    
    # Increment view count
    if job:
        increment_job_views(job_id)
    
    return job
