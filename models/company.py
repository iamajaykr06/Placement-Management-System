from db import get_db_connection

def get_user_id_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    cursor.close()
    return user["id"] if user else None

def save_company_profile(user_id, company_name,hr_email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO companies (user_id,company_name,hr_email) VALUES (%s, %s, %s)",
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
