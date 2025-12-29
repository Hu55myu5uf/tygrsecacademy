"""
Capstone Project Models
Defines database models for tier capstone projects and student submissions
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import enum


class SubmissionStatus(str, enum.Enum):
    """Capstone submission status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    GRADED = "graded"
    APPROVED = "approved"
    REJECTED = "rejected"


class CapstoneTier(Base):
    """Capstone project requirements for each tier"""
    __tablename__ = "capstone_tiers"

    id = Column(Integer, primary_key=True, index=True)
    tier_id = Column(Integer, ForeignKey("tiers.id"), unique=True, nullable=False)
    
    # Project details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)  # Markdown format
    deliverables = Column(JSON, nullable=False)  # List of required deliverables
    rubric = Column(JSON, nullable=False)  # Grading criteria with point values
    
    # Scoring
    max_score = Column(Integer, default=100, nullable=False)
    passing_score = Column(Integer, default=70, nullable=False)
    
    # Constraints
    time_limit_hours = Column(Integer, nullable=True)  # Null = unlimited
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tier = relationship("Tier", backref="capstone")
    submissions = relationship("CapstoneSubmission", back_populates="capstone_tier")

    def __repr__(self):
        return f"<CapstoneTier(tier_id={self.tier_id}, title={self.title})>"


class CapstoneSubmission(Base):
    """Student capstone project submissions"""
    __tablename__ = "capstone_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    capstone_tier_id = Column(Integer, ForeignKey("capstone_tiers.id"), nullable=False)
    
    # Submission content
    github_url = Column(String(500), nullable=True)
    documentation_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    write_up = Column(Text, nullable=True)  # Markdown write-up
    files_json = Column(JSON, nullable=True)  # Metadata for uploaded files
    
    # Status tracking
    status = Column(SQLEnum(SubmissionStatus), default=SubmissionStatus.DRAFT, nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Grading
    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    graded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Rubric evaluation (JSON with points awarded per criterion)
    rubric_evaluation = Column(JSON, nullable=True)
    
    # Showcase
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="capstone_submissions")
    capstone_tier = relationship("CapstoneTier", back_populates="submissions")
    grader = relationship("User", foreign_keys=[graded_by])

    def __repr__(self):
        return f"<CapstoneSubmission(id={self.id}, user_id={self.user_id}, status={self.status})>"
