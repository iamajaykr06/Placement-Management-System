"""
Database Migration Script
This script helps migrate from the old schema to the improved schema.
Run this script after backing up your database.
"""

import mysql.connector
from db import get_db_connection

def migrate_database():
    """Migrate database to improved schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    try:
        # Add new columns to users table
        print("1. Updating users table...")
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
            print("   ✓ Added is_active column")
        except mysql.connector.Error as e:
            if "Duplicate column name" not in str(e):
                print(f"   ⚠ is_active: {e}")
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE")
            print("   ✓ Added email_verified column")
        except mysql.connector.Error as e:
            if "Duplicate column name" not in str(e):
                print(f"   ⚠ email_verified: {e}")
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP NULL")
            print("   ✓ Added last_login column")
        except mysql.connector.Error as e:
            if "Duplicate column name" not in str(e):
                print(f"   ⚠ last_login: {e}")
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            print("   ✓ Added updated_at column")
        except mysql.connector.Error as e:
            if "Duplicate column name" not in str(e):
                print(f"   ⚠ updated_at: {e}")
        
        # Add indexes to users table
        try:
            cursor.execute("CREATE INDEX idx_email ON users(email)")
            print("   ✓ Added email index")
        except mysql.connector.Error as e:
            if "Duplicate key name" not in str(e):
                print(f"   ⚠ idx_email: {e}")
        
        # Add new columns to students table
        print("\n2. Updating students table...")
        new_student_columns = [
            ("phone", "VARCHAR(20)"),
            ("year_of_study", "INT"),
            ("skills", "TEXT"),
            ("resume_url", "VARCHAR(500)"),
            ("linkedin_url", "VARCHAR(500)"),
            ("github_url", "VARCHAR(500)"),
            ("bio", "TEXT"),
            ("is_profile_complete", "BOOLEAN DEFAULT FALSE"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        for col_name, col_type in new_student_columns:
            try:
                cursor.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")
                print(f"   ✓ Added {col_name} column")
            except mysql.connector.Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"   ⚠ {col_name}: {e}")
        
        # Add CGPA constraint
        try:
            cursor.execute("ALTER TABLE students ADD CONSTRAINT chk_cgpa CHECK (cgpa >= 0 AND cgpa <= 10)")
            print("   ✓ Added CGPA constraint")
        except mysql.connector.Error as e:
            if "Duplicate" not in str(e):
                print(f"   ⚠ CGPA constraint: {e}")
        
        # Add new columns to companies table
        print("\n3. Updating companies table...")
        new_company_columns = [
            ("company_type", "VARCHAR(100)"),
            ("industry", "VARCHAR(100)"),
            ("website", "VARCHAR(500)"),
            ("hr_phone", "VARCHAR(20)"),
            ("address", "TEXT"),
            ("description", "TEXT"),
            ("logo_url", "VARCHAR(500)"),
            ("is_verified", "BOOLEAN DEFAULT FALSE"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        for col_name, col_type in new_company_columns:
            try:
                cursor.execute(f"ALTER TABLE companies ADD COLUMN {col_name} {col_type}")
                print(f"   ✓ Added {col_name} column")
            except mysql.connector.Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"   ⚠ {col_name}: {e}")
        
        # Add new columns to jobs table
        print("\n4. Updating jobs table...")
        new_job_columns = [
            ("requirements", "TEXT"),
            ("location", "VARCHAR(255)"),
            ("job_type", "ENUM('full-time', 'part-time', 'internship', 'contract') DEFAULT 'full-time'"),
            ("salary_min", "DECIMAL(10, 2)"),
            ("salary_max", "DECIMAL(10, 2)"),
            ("currency", "VARCHAR(10) DEFAULT 'INR'"),
            ("application_deadline", "DATE"),
            ("max_applications", "INT DEFAULT 100"),
            ("current_applications", "INT DEFAULT 0"),
            ("views_count", "INT DEFAULT 0"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        for col_name, col_type in new_job_columns:
            try:
                cursor.execute(f"ALTER TABLE jobs ADD COLUMN {col_name} {col_type}")
                print(f"   ✓ Added {col_name} column")
            except mysql.connector.Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"   ⚠ {col_name}: {e}")
        
        # Update jobs status enum
        try:
            cursor.execute("ALTER TABLE jobs MODIFY COLUMN status ENUM('active', 'inactive', 'closed', 'draft') DEFAULT 'active'")
            print("   ✓ Updated status enum")
        except mysql.connector.Error as e:
            print(f"   ⚠ status enum: {e}")
        
        # Add new columns to applications table
        print("\n5. Updating applications table...")
        new_application_columns = [
            ("cover_letter", "TEXT"),
            ("reviewed_at", "TIMESTAMP NULL"),
            ("notes", "TEXT")
        ]
        
        for col_name, col_type in new_application_columns:
            try:
                cursor.execute(f"ALTER TABLE applications ADD COLUMN {col_name} {col_type}")
                print(f"   ✓ Added {col_name} column")
            except mysql.connector.Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"   ⚠ {col_name}: {e}")
        
        # Update applications status enum
        try:
            cursor.execute("ALTER TABLE applications MODIFY COLUMN status ENUM('pending', 'reviewed', 'shortlisted', 'accepted', 'rejected', 'withdrawn') DEFAULT 'pending'")
            print("   ✓ Updated status enum")
        except mysql.connector.Error as e:
            print(f"   ⚠ status enum: {e}")
        
        # Create notifications table
        print("\n6. Creating notifications table...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    link VARCHAR(500),
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_is_read (is_read),
                    INDEX idx_created_at (created_at),
                    INDEX idx_type (type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("   ✓ Created notifications table")
        except mysql.connector.Error as e:
            if "already exists" not in str(e).lower():
                print(f"   ⚠ notifications table: {e}")
        
        # Create activity_logs table
        print("\n7. Creating activity_logs table...")
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(100) NOT NULL,
                    entity_type VARCHAR(50),
                    entity_id INT,
                    details TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_user_id (user_id),
                    INDEX idx_action (action),
                    INDEX idx_entity (entity_type, entity_id),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("   ✓ Created activity_logs table")
        except mysql.connector.Error as e:
            if "already exists" not in str(e).lower():
                print(f"   ⚠ activity_logs table: {e}")
        
        # Update existing records
        print("\n8. Updating existing records...")
        try:
            # Mark existing students with complete profiles
            cursor.execute("""
                UPDATE students 
                SET is_profile_complete = TRUE 
                WHERE name IS NOT NULL AND name != '' 
                AND email IS NOT NULL AND email != ''
                AND course IS NOT NULL AND course != ''
                AND cgpa > 0
            """)
            print(f"   ✓ Updated {cursor.rowcount} student profiles")
        except mysql.connector.Error as e:
            print(f"   ⚠ Update students: {e}")
        
        # Initialize current_applications count
        try:
            cursor.execute("""
                UPDATE jobs j
                SET current_applications = (
                    SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id
                )
            """)
            print(f"   ✓ Updated application counts for {cursor.rowcount} jobs")
        except mysql.connector.Error as e:
            print(f"   ⚠ Update application counts: {e}")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        print("\nNote: Some indexes and constraints may need to be added manually.")
        print("Refer to database_schema_improved.sql for complete schema.")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration Tool")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Backup your database before running this script!")
    print("\nThis script will:")
    print("1. Add new columns to existing tables")
    print("2. Create new tables (notifications, activity_logs)")
    print("3. Update existing records")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")
    
    try:
        input()
        migrate_database()
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
