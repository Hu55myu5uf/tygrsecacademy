"""
User Models
Database models for users, authentication, and profiles
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration"""
    STUDENT = "student"
    TUTOR = "tutor"
    ADMIN = "admin"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Bio and profile
    bio = Column(Text)
    avatar_url = Column(Text)  # Changed from String(500) to Text for base64 images
    linkedin_url = Column(String(500))
    github_url = Column(String(500))
    
    # Additional profile information
    date_of_birth = Column(DateTime(timezone=False), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    lab_instances = relationship("LabInstance", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT
    
    @property
    def is_tutor(self) -> bool:
        return self.role == UserRole.TUTOR
    
    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


class RefreshToken(Base):
    """Refresh token storage for JWT authentication"""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<RefreshToken(user_id={self.user_id}, revoked={self.is_revoked})>"
