"""
Challenge Models
Database models for CTF challenges, submissions, and leaderboards
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from database.connection import Base
import enum


class ChallengeDifficulty(str, enum.Enum):
    """Challenge difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    INSANE = "insane"


class ChallengeCategory(str, enum.Enum):
    """Challenge categories"""
    OSINT = "osint"
    MALWARE_ANALYSIS = "malware_analysis"
    WEB_SECURITY = "web_security"
    CRYPTOGRAPHY = "cryptography"
    FORENSICS = "forensics"
    REVERSE_ENGINEERING = "reverse_engineering"
    ADVERSARIAL_ML = "adversarial_ml"
    NETWORK_SECURITY = "network_security"
    EXPLOITATION = "exploitation"


class Challenge(Base):
    """CTF challenge definition"""
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    
    # Classification
    category = Column(SQLEnum(ChallengeCategory), nullable=False)
    difficulty = Column(SQLEnum(ChallengeDifficulty), nullable=False)
    
    # Content
    instructions = Column(Text)
    files_url = Column(String(500))  # URL to challenge files
    
    # Flag
    flag = Column(String(200), nullable=False)
    flag_format = Column(String(100))  # e.g., "TYGR{.*}"
    
    # Scoring
    base_points = Column(Integer, nullable=False)  # Base points for solving
    hint_penalty = Column(Integer, default=10)  # Percentage penalty per hint
    
    # AI assistance
    ai_assistance_enabled = Column(Boolean, default=True)
    
    # Metadata
    author = Column(String(200))
    tags = Column(JSON)  # List of tags
    
    # Status
    is_published = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Challenge(id={self.id}, title='{self.title}', difficulty='{self.difficulty}')>"


class ChallengeSubmission(Base):
    """Student challenge submission"""
    __tablename__ = "challenge_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Submission
    submitted_flag = Column(String(200), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    
    # Scoring
    points_earned = Column(Integer)
    hints_used = Column(Integer, default=0)
    
    # Timing
    time_to_solve_minutes = Column(Integer)  # Time from first view to solve
    
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ChallengeSubmission(id={self.id}, correct={self.is_correct})>"


class ChallengeHint(Base):
    """Hints for challenges"""
    __tablename__ = "challenge_hints"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    
    hint_level = Column(Integer, nullable=False)  # Progressive hints
    hint_text = Column(Text, nullable=False)
    penalty_percent = Column(Integer, nullable=False)
    
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ChallengeHint(challenge_id={self.challenge_id}, level={self.hint_level})>"


class Leaderboard(Base):
    """Challenge leaderboard entries"""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Scores
    total_points = Column(Integer, default=0, nullable=False)
    challenges_solved = Column(Integer, default=0, nullable=False)
    
    # Rankings by difficulty
    easy_solved = Column(Integer, default=0)
    medium_solved = Column(Integer, default=0)
    hard_solved = Column(Integer, default=0)
    insane_solved = Column(Integer, default=0)
    
    # Metadata
    rank = Column(Integer)  # Overall rank
    last_solve_at = Column(DateTime(timezone=True))
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Leaderboard(user_id={self.user_id}, points={self.total_points}, rank={self.rank})>"
