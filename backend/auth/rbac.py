"""
Role-Based Access Control (RBAC)
Decorators and middleware for permission checking
"""
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.connection import get_db
from models.user import User, UserRole
from auth.jwt_handler import decode_token

# Security scheme for bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    
    # Get user ID from payload
    user_id = int(payload.get("sub"))
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (additional check)
    
    Args:
        current_user: Current user from token
        
    Returns:
        Active user object
    """
    return current_user


def require_role(allowed_roles: List[UserRole]):
    """
    Dependency to require specific roles
    
    Args:
        allowed_roles: List of roles that are allowed
        
    Returns:
        Dependency function
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    
    return role_checker


# Convenience functions for common role requirements
def require_student():
    """Require student role"""
    return require_role([UserRole.STUDENT, UserRole.TUTOR, UserRole.ADMIN])


def require_tutor():
    """Require tutor role or higher"""
    return require_role([UserRole.TUTOR, UserRole.ADMIN])


def require_admin():
    """Require admin role"""
    return require_role([UserRole.ADMIN])
