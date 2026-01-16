from db import get_db_connection

# get user_id of logged user by username

def get_user_id_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user["id"] if user else None

# To save the data of student
def save_student_profile(user_id: object, name: object, email: object, course: object, cgpa: object) -> None:
    """

    :rtype: None
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (user_id,name,email,course,cgpa) VALUES (%s, %s, %s, %s)",
        (user_id,name, email, course, cgpa)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
# To show student profile details

def get_student_profile(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM students WHERE user_id = %s",
        (user_id,)
    )
    
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return profile