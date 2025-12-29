
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database.connection import Base

class LabDifficulty(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class LabType(str, enum.Enum):
    TERMINAL = "terminal"  # WebSocket-based terminal (Alpine, etc.)
    GUACAMOLE = "guacamole"  # VNC/RDP via Apache Guacamole

class LabInstanceStatus(str, enum.Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    docker_image = Column(String, nullable=False)  # e.g., "tygrsec/lab-basic-01"
    difficulty = Column(String, default=LabDifficulty.BEGINNER)
    category = Column(String, default="General")
    content = Column(String, nullable=True)  # Markdown instructions
    estimated_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Lab Type fields
    lab_type = Column(String, default=LabType.TERMINAL)  # terminal or guacamole
    guacamole_url = Column(String, nullable=True)  # URL to Guacamole connection (for guacamole type)
    compose_file = Column(String, nullable=True)  # Path to docker-compose.yml for complex labs

    # Relationships
    instances = relationship("LabInstance", back_populates="lab")

class LabInstance(Base):
    __tablename__ = "lab_instances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lab_id = Column(Integer, ForeignKey("labs.id"))
    container_id = Column(String, nullable=True)
    status = Column(String, default=LabInstanceStatus.STARTING)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="lab_instances")
    lab = relationship("Lab", back_populates="instances")

# Update User model to include relationship (will need to be done in user model file or monkey patched if lazy)
# Ideally we update models/user.py
