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

def save_company_profile(user_id, company_name=None, hr_email=None, company_type=None,
                        industry=None, website=None, hr_phone=None, address=None,
                        description=None, logo_url=None):
    """
    Save or update company profile with all available fields.
    Only updates fields that are provided (not None).
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get existing profile
    cursor.execute("SELECT * FROM companies WHERE user_id = %s", (user_id,))
    existing = cursor.fetchone()
    
    # Prepare update values
    update_fields = []
    values = []
    
    fields_map = {
        'company_name': company_name,
        'hr_email': hr_email,
        'company_type': company_type,
        'industry': industry,
        'website': website,
        'hr_phone': hr_phone,
        'address': address,
        'description': description,
        'logo_url': logo_url
    }
    
    for field, value in fields_map.items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            values.append(value)
    
    if existing:
        # Update existing profile
        if update_fields:
            values.append(user_id)
            query = f"""
                UPDATE companies 
                SET {', '.join(update_fields)}
                WHERE user_id = %s
            """
            cursor.execute(query, values)
    else:
        # Insert new profile
        insert_fields = ['user_id'] + [k for k, v in fields_map.items() if v is not None]
        insert_values = [user_id] + [v for v in fields_map.values() if v is not None]
        
        placeholders = ', '.join(['%s'] * len(insert_values))
        query = f"""
            INSERT INTO companies ({', '.join(insert_fields)})
            VALUES ({placeholders})
        """
        cursor.execute(query, insert_values)

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

def get_company_by_id(company_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM companies WHERE id = %s",
        (company_id,)
    )
    company = cursor.fetchone()
    cursor.close()
    conn.close()
    return company