"""
Audit Models
Database models for audit logging and security events
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database.connection import Base


class AuditLog(Base):
    """Comprehensive audit log for all user actions"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Nullable for anonymous actions
    
    # Action details
    action = Column(String(200), nullable=False)  # login, view_lesson, submit_flag, etc.
    resource_type = Column(String(100))  # user, lesson, lab, challenge, etc.
    resource_id = Column(Integer)
    
    # Request details
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))
    request_method = Column(String(10))  # GET, POST, etc.
    request_path = Column(String(500))
    
    # Additional data
    extra_data = Column(JSON)  # Additional context as JSON
    
    # Status
    success = Column(String(20))  # Boolean or failed/success
    error_message = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', user_id={self.user_id})>"


class SecurityEvent(Base):
    """Security-related events for monitoring"""
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Event details
    event_type = Column(String(100), nullable=False)  # failed_login, suspicious_activity, etc.
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    description = Column(Text)
    
    # Context
    ip_address = Column(String(45))
    extra_data = Column(JSON)
    
    # Resolution
    is_resolved = Column(String(20), default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<SecurityEvent(id={self.id}, type='{self.event_type}', severity='{self.severity}')>"
