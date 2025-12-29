"""
Password Handler
Secure password hashing and verification using bcrypt
"""
from passlib.context import CryptContext
from config import settings

# Handle passlib compatibility with bcrypt 4.0+
import bcrypt
try:
    if not hasattr(bcrypt, "__about__"):
        # Passlib expects bcrypt.__about__.__version__
        class About:
            __version__ = getattr(bcrypt, "__version__", "4.0.0")
        bcrypt.__about__ = About()
except Exception:
    pass

# Create password context with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_COST_FACTOR
)


def hash_password(password: str) -> str:
    """
    Hash a plain password
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    # Bcrypt has a maximum password length of 72 bytes.
    # We truncate the string such that its UTF-8 encoding is at most 72 bytes.
    password_bytes = password.encode('utf-8')[:72]
    truncated_password = password_bytes.decode('utf-8', 'ignore')
    return pwd_context.hash(truncated_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hash to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    # Truncate to 72 bytes for bcrypt compatibility
    encoded = plain_password.encode('utf-8')[:72]
    truncated_password = encoded.decode('utf-8', 'ignore')
    return pwd_context.verify(truncated_password, hashed_password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 72:
        return False, "Password must be 72 characters or less"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        return False, "Password must contain at least one special character"
    
    return True, ""
