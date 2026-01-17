from db import get_db_connection

def get_company_id_by_user_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM companies WHERE user_id = %s",
        (user_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row["id"] if row else None

def save_company_profile(user_id, company_name, hr_email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO companies (user_id, company_name, hr_email)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            company_name = VALUES(company_name),
            hr_email = VALUES(hr_email)
        """,
        (user_id, company_name, hr_email)
    )

    conn.commit()
    cursor.close()
    conn.close()

def get_company_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM companies WHERE user_id = %s",
        (user_id,)
    )
    company = cursor.fetchone()
    cursor.close()
    conn.close()
    return company
