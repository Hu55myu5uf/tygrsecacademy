"""
Publishing Models
Database models for capstone projects and blog publishing
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from database.connection import Base
import enum


class CapstoneStatus(str, enum.Enum):
    """Capstone project status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"


class Capstone(Base):
    """Student capstone project"""
    __tablename__ = "capstones"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tutor_id = Column(Integer, ForeignKey("users.id"))  # Assigned tutor
    
    # Content
    title = Column(String(300), nullable=False)
    description = Column(Text)
    content_markdown = Column(Text)
    
    # Files
    files_url = Column(String(500))  # URL to project files
    
    # Status
    status = Column(SQLEnum(CapstoneStatus), default=CapstoneStatus.DRAFT, nullable=False)
    
    # Review
    tutor_feedback = Column(Text)
    score = Column(Integer)  # Out of 100
    
    # Timestamps
    submitted_at = Column(DateTime(timezone=True))
    reviewed_at = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Capstone(id={self.id}, user_id={self.user_id}, status='{self.status}')>"


class BlogPost(Base):
    """Published blog posts (approved capstones and articles)"""
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    capstone_id = Column(Integer, ForeignKey("capstones.id"))  # If from capstone
    
    # Content
    title = Column(String(300), nullable=False)
    slug = Column(String(350), unique=True, nullable=False)  # URL-friendly title
    summary = Column(Text)
    content_markdown = Column(Text, nullable=False)
    
    # Metadata
    cover_image_url = Column(String(500))
    tags = Column(String(500))  # Comma-separated tags
    
    # Stats
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    
    # Publishing
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<BlogPost(id={self.id}, title='{self.title}')>"


class ExternalShare(Base):
    """Tracking external shares (LinkedIn, etc.)"""
    __tablename__ = "external_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_post_id = Column(Integer, ForeignKey("blog_posts.id"))
    capstone_id = Column(Integer, ForeignKey("capstones.id"))
    
    platform = Column(String(100), nullable=False)  # linkedin, twitter, medium, etc.
    share_url = Column(String(500))
    
    shared_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ExternalShare(id={self.id}, platform='{self.platform}')>"
