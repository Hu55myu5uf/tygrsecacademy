"""
AI Context Models
Database models for AI conversation history and recommendations
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database.connection import Base


class AIConversation(Base):
    """AI tutor conversation history"""
    __tablename__ = "ai_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Context
    context_type = Column(String(50), nullable=False)  # lesson, lab, challenge
    context_id = Column(Integer, nullable=False)  # ID of lesson/lab/challenge
    
    # Conversation
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    
    # Metadata
    tokens_used = Column(Integer)
    response_time_ms = Column(Integer)
    model_used = Column(String(100))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AIConversation(id={self.id}, user_id={self.user_id}, context='{self.context_type}')>"


class AIRecommendation(Base):
    """AI-generated content recommendations"""
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Recommendation
    recommendation_type = Column(String(50), nullable=False)  # next_module, challenge, etc.
    recommended_id = Column(Integer, nullable=False)  # ID of recommended item
    reason = Column(Text)  # Why this was recommended
    
    # Engagement
    was_viewed = Column(String(20), default=False)
    was_accepted = Column(String(20), default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AIRecommendation(id={self.id}, type='{self.recommendation_type}')>"
