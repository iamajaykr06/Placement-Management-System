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

def save_student_profile(user_id, name=None, email=None, course=None, cgpa=None, 
                        phone=None, year_of_study=None, skills=None, bio=None,
                        resume_url=None, linkedin_url=None, github_url=None):
    """
    Save or update student profile with all available fields.
    Only updates fields that are provided (not None).
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    # Get existing profile to merge with new data
    cur.execute("SELECT * FROM students WHERE user_id = %s", (user_id,))
    existing = cur.fetchone()
    
    # Prepare update values
    update_fields = []
    values = []
    
    fields_map = {
        'name': name,
        'email': email,
        'course': course,
        'cgpa': cgpa,
        'phone': phone,
        'year_of_study': year_of_study,
        'skills': skills,
        'bio': bio,
        'resume_url': resume_url,
        'linkedin_url': linkedin_url,
        'github_url': github_url
    }
    
    for field, value in fields_map.items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    # Check if profile is complete
    is_complete = bool(name and email and course and cgpa)
    if is_complete:
        update_fields.append("is_profile_complete = TRUE")
    
    if existing:
        # Update existing profile
        if update_fields:
            values.append(user_id)
            query = f"""
                UPDATE students 
                SET {', '.join(update_fields)}
                WHERE user_id = %s
            """
            cur.execute(query, values)
    else:
        # Insert new profile
        insert_fields = ['user_id'] + [k for k, v in fields_map.items() if v is not None]
        if is_complete:
            insert_fields.append('is_profile_complete')
        
        insert_values = [user_id] + [v for v in fields_map.values() if v is not None]
        if is_complete:
            insert_values.append(True)
        
        placeholders = ', '.join(['%s'] * len(insert_values))
        query = f"""
            INSERT INTO students ({', '.join(insert_fields)})
            VALUES ({placeholders})
        """
        cur.execute(query, insert_values)

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