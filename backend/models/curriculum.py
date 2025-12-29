"""
Curriculum Models
Database models for tiers, modules, lessons, and content
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import enum


class ContentType(str, enum.Enum):
    """Content block type enumeration"""
    TEXT = "text"
    CODE = "code"
    VIDEO = "video"
    IMAGE = "image"
    QUIZ = "quiz"


class Tier(Base):
    """Curriculum tier (0-4)"""
    __tablename__ = "tiers"
    
    id = Column(Integer, primary_key=True, index=True)
    tier_number = Column(Integer, unique=True, nullable=False, index=True)  # 0, 1, 2, 3, 4
    name = Column(String(200), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    modules = relationship("Module", back_populates="tier", lazy="select")
    
    def __repr__(self):
        return f"<Tier(tier={self.tier_number}, name='{self.name}')>"


class Module(Base):
    """Learning module within a tier"""
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    tier_id = Column(Integer, ForeignKey("tiers.id"), nullable=False)
    
    title = Column(String(300), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    
    # Requirements
    estimated_hours = Column(Integer)  # Estimated completion time
    prerequisites = Column(Text)  # Comma-separated module IDs or description
    
    # Status
    is_published = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tier = relationship("Tier", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", lazy="select", order_by="Lesson.order")
    
    def __repr__(self):
        return f"<Module(id={self.id}, title='{self.title}')>"


class Lesson(Base):
    """Individual lesson within a module"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    
    title = Column(String(300), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    
    # Content
    content_markdown = Column(Text)  # Main markdown content
    
    # Metadata
    duration_minutes = Column(Integer)
    difficulty = Column(String(50))  # beginner, intermediate, advanced
    
    # Status
    is_published = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    module = relationship("Module", back_populates="lessons")
    content_blocks = relationship("ContentBlock", back_populates="lesson", lazy="select", order_by="ContentBlock.order")
    
    # CTF Link
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=True)
    challenge = relationship("Challenge", backref="lesson", lazy="select")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}')>"



class ContentBlock(Base):
    """Rich content blocks within a lesson"""
    __tablename__ = "content_blocks"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    type = Column(SQLEnum(ContentType), nullable=False)
    order = Column(Integer, nullable=False)
    
    # Content (varies by type)
    text_content = Column(Text)  # For text and markdown
    code_content = Column(Text)  # For code blocks
    code_language = Column(String(50))  # Programming language
    media_url = Column(String(500))  # For video/image URLs
    quiz_data = Column(Text)  # JSON string for quiz questions
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lesson = relationship("Lesson", back_populates="content_blocks")
    
    def __repr__(self):
        return f"<ContentBlock(id={self.id}, type='{self.type}')>"

