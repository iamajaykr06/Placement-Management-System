from db import get_db_connection

def get_company_id_by_user_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT id FROM companies WHERE user_id = %s",
        (user_id,)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row["id"] if row else None


def create_job(company_id, title, description, eligibility):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO jobs (company_id, title, description, eligibility)
        VALUES (%s, %s, %s, %s)
        """,
        (company_id, title, description, eligibility)
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
        "SELECT * FROM jobs WHERE status = 'active'"
    )

    jobs = cur.fetchall()
    cur.close()
    conn.close()
    return jobs

def get_job_by_id(job_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM jobs WHERE id = %s",
        (job_id,)
    )

    job = cur.fetchone()
    cur.close()
    conn.close()
    return job
