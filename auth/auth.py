"""
Authentication utilities for password hashing and verification.
Includes password strength validation and security features.
"""
import re
from werkzeug.security import generate_password_hash, check_password_hash

# Password hashing method - using pbkdf2:sha256 (default, secure)
# You can customize the method if needed
PASSWORD_HASH_METHOD = 'pbkdf2:sha256:600000'

def hash_password(password):
    """
    Hash a password using werkzeug's secure password hashing.
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Hashed password string
        
    Raises:
        ValueError: If password is empty or None
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    
    return generate_password_hash(password, method=PASSWORD_HASH_METHOD.split(':')[0])


def verify_password(password, hashed_password):
    """
    Verify a password against its hash.
    
    Args:
        password (str): Plain text password to verify
        hashed_password (str): Hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    if not password or not hashed_password:
        return False
    
    try:
        return check_password_hash(hashed_password, password)
    except Exception:
        return False


def validate_password_strength(password):
    """
    Validate password strength.
    
    Requirements:
    - Minimum 6 characters
    - At least one letter
    - At least one number (optional but recommended)
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    # Check for at least one letter
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    # Optional: Check for at least one number (recommended)
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    # Optional: Check for special characters (recommended)
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"


def validate_password_strength_medium(password):
    """
    Medium strength password validation (less strict).
    
    Requirements:
    - Minimum 6 characters
    - At least one letter
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    # Check for at least one letter
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    return True, "Password is valid"


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username):
    """
    Validate username format.
    
    Requirements:
    - 3-30 characters
    - Alphanumeric, underscore, and hyphen only
    - Must start with a letter or number
    
    Args:
        username (str): Username to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not username:
        return False, "Username cannot be empty"
    
    username = username.strip()
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    
    # Only alphanumeric, underscore, and hyphen
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscore, and hyphen"
    
    # Must start with letter or number
    if not re.match(r'^[a-zA-Z0-9]', username):
        return False, "Username must start with a letter or number"
    
    return True, "Username is valid"


def generate_secure_token(length=32):
    """
    Generate a secure random token (for password reset, email verification, etc.).
    
    Args:
        length (int): Length of the token (default: 32)
        
    Returns:
        str: Secure random token
    """
    import secrets
    return secrets.token_urlsafe(length)


def sanitize_input(input_string, max_length=None):
    """
    Sanitize user input by removing potentially dangerous characters.
    
    Args:
        input_string (str): Input string to sanitize
        max_length (int): Maximum length allowed
        
    Returns:
        str: Sanitized string
    """
    if not input_string:
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = input_string.strip()
    
    # Remove null bytes and control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
