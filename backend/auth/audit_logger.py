"""
Audit Logger
Comprehensive logging for security and user actions
"""
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Request

from models.audit import AuditLog, SecurityEvent

logger = logging.getLogger(__name__)


def log_action(
    db: Session,
    action: str,
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[int] = None,
    request: Optional[Request] = None,
    success: bool = True,
    metadata: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
) -> AuditLog:
    """
    Log a user action to the audit log
    
    Args:
        db: Database session
        action: Action being performed
        user_id: ID of user performing action
        resource_type: Type of resource being accessed
        resource_id: ID of resource being accessed
        request: FastAPI request object
        success: Whether action was successful
        metadata: Additional context
        error_message: Error message if action failed
        
    Returns:
        Created audit log entry
    """
    # Extract request details if provided
    ip_address = None
    user_agent = None
    request_method = None
    request_path = None
    
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        request_method = request.method
        request_path = str(request.url.path)
    
    # Create audit log entry
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        request_method=request_method,
        request_path=request_path,
        success="success" if success else "failed",
        extra_data=metadata,
        error_message=error_message
    )
    
    db.add(audit_log)
    db.commit()
    
    logger.info(f"Audit: {action} by user {user_id} - {success}")
    
    return audit_log


def log_security_event(
    db: Session,
    event_type: str,
    severity: str,
    description: str,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> SecurityEvent:
    """
    Log a security event
    
    Args:
        db: Database session
        event_type: Type of security event
        severity: Severity level (low, medium, high, critical)
        description: Description of the event
        user_id: ID of user involved
        ip_address: IP address involved
        metadata: Additional context
        
    Returns:
        Created security event entry
    """
    security_event = SecurityEvent(
        user_id=user_id,
        event_type=event_type,
        severity=severity,
        description=description,
        ip_address=ip_address,
        extra_data=metadata,
        is_resolved="false"
    )
    
    db.add(security_event)
    db.commit()
    
    logger.warning(f"Security Event [{severity}]: {event_type} - {description}")
    
    return security_event


def log_login_attempt(
    db: Session,
    email: str,
    success: bool,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    reason: Optional[str] = None
):
    """
    Log a login attempt
    
    Args:
        db: Database session
        email: Email used for login
        success: Whether login was successful
        user_id: User ID if successful
        ip_address: IP address of attempt
        reason: Reason for failure if unsuccessful
    """
    if success:
        log_action(
            db=db,
            action="login_success",
            user_id=user_id,
            metadata={"email": email, "ip": ip_address},
            success=True
        )
    else:
        log_security_event(
            db=db,
            event_type="failed_login",
            severity="medium",
            description=f"Failed login attempt for {email}: {reason}",
            ip_address=ip_address,
            metadata={"email": email, "reason": reason}
        )


def log_password_change(
    db: Session,
    user_id: int,
    ip_address: Optional[str] = None
):
    """Log a password change"""
    log_action(
        db=db,
        action="password_change",
        user_id=user_id,
        metadata={"ip": ip_address},
        success=True
    )
    
    log_security_event(
        db=db,
        event_type="password_changed",
        severity="low",
        description=f"User {user_id} changed password",
        user_id=user_id,
        ip_address=ip_address
    )
