-- =====================================================
-- IMPROVED Placement Management System Database Schema
-- =====================================================
-- This schema includes better indexes, constraints, and additional fields
-- for improved performance and functionality

CREATE DATABASE IF NOT EXISTS placement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE placement_db;

-- =====================================================
-- USERS TABLE (Authentication & Authorization)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'company', 'admin') NOT NULL DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for better query performance
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_role (role),
    INDEX idx_is_active (is_active),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- STUDENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    course VARCHAR(100),
    year_of_study INT,
    cgpa DECIMAL(4, 2) CHECK (cgpa >= 0 AND cgpa <= 10),
    skills TEXT,
    resume_url VARCHAR(500),
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    bio TEXT,
    is_profile_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_course (course),
    INDEX idx_cgpa (cgpa),
    INDEX idx_is_profile_complete (is_profile_complete),
    FULLTEXT INDEX idx_skills (skills)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- COMPANIES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    company_name VARCHAR(255) NOT NULL,
    company_type VARCHAR(100),
    industry VARCHAR(100),
    website VARCHAR(500),
    hr_email VARCHAR(255),
    hr_phone VARCHAR(20),
    address TEXT,
    description TEXT,
    logo_url VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_company_name (company_name),
    INDEX idx_industry (industry),
    INDEX idx_is_verified (is_verified),
    FULLTEXT INDEX idx_description (description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- JOBS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    eligibility TEXT,
    location VARCHAR(255),
    job_type ENUM('full-time', 'part-time', 'internship', 'contract') DEFAULT 'full-time',
    salary_min DECIMAL(10, 2),
    salary_max DECIMAL(10, 2),
    currency VARCHAR(10) DEFAULT 'INR',
    status ENUM('active', 'inactive', 'closed', 'draft') DEFAULT 'active',
    application_deadline DATE,
    max_applications INT DEFAULT 100,
    current_applications INT DEFAULT 0,
    views_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    
    -- Indexes for better performance
    INDEX idx_company_id (company_id),
    INDEX idx_status (status),
    INDEX idx_job_type (job_type),
    INDEX idx_created_at (created_at),
    INDEX idx_application_deadline (application_deadline),
    INDEX idx_location (location),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- APPLICATIONS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    job_id INT NOT NULL,
    status ENUM('pending', 'reviewed', 'shortlisted', 'accepted', 'rejected', 'withdrawn') DEFAULT 'pending',
    cover_letter TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    notes TEXT,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    
    -- Unique constraint to prevent duplicate applications
    UNIQUE KEY unique_application (student_id, job_id),
    
    -- Indexes
    INDEX idx_student_id (student_id),
    INDEX idx_job_id (job_id),
    INDEX idx_status (status),
    INDEX idx_applied_at (applied_at),
    INDEX idx_reviewed_at (reviewed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- NOTIFICATIONS TABLE (Optional - for future enhancement)
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ACTIVITY LOG TABLE (Optional - for audit trail)
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Trigger to update application count when new application is created
DELIMITER //
CREATE TRIGGER update_job_application_count_insert
AFTER INSERT ON applications
FOR EACH ROW
BEGIN
    UPDATE jobs 
    SET current_applications = current_applications + 1 
    WHERE id = NEW.job_id;
END//

-- Trigger to update application count when application is deleted
CREATE TRIGGER update_job_application_count_delete
AFTER DELETE ON applications
FOR EACH ROW
BEGIN
    UPDATE jobs 
    SET current_applications = GREATEST(current_applications - 1, 0)
    WHERE id = OLD.job_id;
END//

DELIMITER ;

-- =====================================================
-- VIEWS FOR COMMON QUERIES (Performance Optimization)
-- =====================================================

-- View for active jobs with company details
CREATE OR REPLACE VIEW vw_active_jobs AS
SELECT 
    j.id,
    j.title,
    j.description,
    j.eligibility,
    j.location,
    j.job_type,
    j.salary_min,
    j.salary_max,
    j.currency,
    j.application_deadline,
    j.current_applications,
    j.views_count,
    j.created_at,
    c.id AS company_id,
    c.company_name,
    c.industry,
    c.logo_url
FROM jobs j
INNER JOIN companies c ON j.company_id = c.id
WHERE j.status = 'active'
AND (j.application_deadline IS NULL OR j.application_deadline >= CURDATE())
AND (j.max_applications IS NULL OR j.current_applications < j.max_applications);

-- View for student applications with job details
CREATE OR REPLACE VIEW vw_student_applications AS
SELECT 
    a.id AS application_id,
    a.status,
    a.applied_at,
    a.reviewed_at,
    s.id AS student_id,
    s.name AS student_name,
    s.email AS student_email,
    s.course,
    s.cgpa,
    j.id AS job_id,
    j.title AS job_title,
    c.company_name,
    c.id AS company_id
FROM applications a
INNER JOIN students s ON a.student_id = s.id
INNER JOIN jobs j ON a.job_id = j.id
INNER JOIN companies c ON j.company_id = c.id;

-- =====================================================
-- STORED PROCEDURES (Optional - for complex operations)
-- =====================================================

DELIMITER //

-- Procedure to get job statistics for a company
CREATE PROCEDURE sp_get_company_job_stats(IN p_company_id INT)
BEGIN
    SELECT 
        COUNT(*) AS total_jobs,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_jobs,
        SUM(current_applications) AS total_applications,
        SUM(views_count) AS total_views
    FROM jobs
    WHERE company_id = p_company_id;
END//

-- Procedure to get student application statistics
CREATE PROCEDURE sp_get_student_app_stats(IN p_student_id INT)
BEGIN
    SELECT 
        COUNT(*) AS total_applications,
        SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
        SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) AS accepted,
        SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) AS rejected
    FROM applications
    WHERE student_id = p_student_id;
END//

DELIMITER ;

-- =====================================================
-- INITIAL DATA (Optional - for testing)
-- =====================================================

-- Insert a default admin user (password: admin123 - CHANGE THIS!)
-- Password hash for 'admin123' using werkzeug
INSERT INTO users (username, email, password, role, is_active, email_verified) 
VALUES ('admin', 'admin@placement.com', 'pbkdf2:sha256:600000$...', 'admin', TRUE, TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- =====================================================
-- PERFORMANCE OPTIMIZATION NOTES
-- =====================================================
-- 1. All foreign keys have indexes for faster joins
-- 2. Frequently queried columns have indexes
-- 3. Full-text indexes on searchable text fields
-- 4. Composite indexes for common query patterns
-- 5. Views for complex queries reduce computation
-- 6. Triggers maintain data consistency automatically
-- 7. Stored procedures for complex operations
-- 8. UTF8MB4 charset for emoji support
-- 9. InnoDB engine for ACID compliance and foreign keys

-- =====================================================
-- MAINTENANCE RECOMMENDATIONS
-- =====================================================
-- 1. Regularly run ANALYZE TABLE on frequently updated tables
-- 2. Monitor slow query log and optimize queries
-- 3. Archive old activity logs periodically
-- 4. Set up database backups (daily recommended)
-- 5. Monitor table sizes and partition if needed
-- 6. Review and optimize indexes based on query patterns
-- 7. Consider read replicas for high-traffic scenarios
