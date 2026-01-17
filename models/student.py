from db import get_db_connection

# get user_id of logged user by username

def get_student_id_by_user_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM students WHERE user_id = %s",
        (user_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row["id"] if row else None

# To save the data of student

def save_student_profile(user_id, name, email, course, cgpa):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO students (user_id, name, email, course, cgpa)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name=%s,
            email=%s,
            course=%s,
            cgpa=%s
        """,
        (
            user_id, name, email, course, cgpa,
            name, email, course, cgpa
        )
    )

    conn.commit()
    cur.close()
    conn.close()

# To show student profile details

def get_student_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True,buffered=True)
    
    cursor.execute(
        "SELECT * FROM students WHERE user_id = %s",
        (user_id,)
    )
    
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return profile