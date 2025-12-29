"""
Progress Tracking Models
Track student progress through lessons, modules, and tiers
"""
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base


class LessonProgress(Base):
    """Track individual lesson completion per student"""
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    time_spent_minutes = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="lesson_progress")
    lesson = relationship("Lesson", backref="progress_records")
    
    def __repr__(self):
        return f"<LessonProgress(user_id={self.user_id}, lesson_id={self.lesson_id}, completed={self.is_completed})>"


class ModuleProgress(Base):
    """Track module-level progress aggregation"""
    __tablename__ = "module_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completion_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="module_progress")
    module = relationship("Module", backref="progress_records")
    
    def __repr__(self):
        return f"<ModuleProgress(user_id={self.user_id}, module_id={self.module_id}, {self.completion_percentage}%)>"


class TierProgress(Base):
    """Track tier-level advancement with unlock system"""
    __tablename__ = "tier_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tier_id = Column(Integer, ForeignKey("tiers.id"), nullable=False)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completion_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False, nullable=False)
    is_unlocked = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="tier_progress")
    tier = relationship("Tier", backref="progress_records")
    
    def __repr__(self):
        return f"<TierProgress(user_id={self.user_id}, tier={self.tier_id}, unlocked={self.is_unlocked})>"


class Achievement(Base):
    """Gamification achievements definitions"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    icon_name = Column(String(50), nullable=True) # e.g. "Trophy", "Award" matching lucide-react
    criteria_type = Column(String(50), nullable=False) # 'tier_complete', 'challenge_solve_count', 'lesson_count'
    criteria_value = Column(Integer, default=0)
    
    xp_reward = Column(Integer, default=0)

    def __repr__(self):
        return f"<Achievement(name={self.name}, type={self.criteria_type})>"


class UserAchievement(Base):
    """Achievements earned by users"""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", backref="earned_achievements")
    achievement = relationship("Achievement")

    def __repr__(self):
        return f"<UserAchievement(user={self.user_id}, achievement={self.achievement_id})>"
