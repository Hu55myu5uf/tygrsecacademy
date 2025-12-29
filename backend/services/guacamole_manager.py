"""
Guacamole Lab Manager
Handles starting/stopping Guacamole-based lab environments via Docker Compose
"""
import subprocess
import os
import time
from typing import Optional, Dict
from sqlalchemy.orm import Session
from models.labs import Lab, LabInstance, LabInstanceStatus, LabType
import logging

logger = logging.getLogger(__name__)

class GuacamoleManager:
    """Manager for Guacamole-based lab environments"""
    
    def __init__(self):
        self.compose_base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "docker", "guacamole"
        )
        self.running_stacks: Dict[int, bool] = {}  # lab_id -> is_running
    
    def start_lab(self, db: Session, user_id: int, lab_id: int) -> LabInstance:
        """
        Start a Guacamole lab environment.
        Uses Docker Compose to spin up the lab stack.
        """
        lab = db.query(Lab).filter(Lab.id == lab_id).first()
        if not lab:
            raise Exception(f"Lab {lab_id} not found")
        
        if lab.lab_type != LabType.GUACAMOLE:
            raise Exception(f"Lab {lab_id} is not a Guacamole lab")
        
        # Check for existing running instance
        existing = db.query(LabInstance).filter(
            LabInstance.user_id == user_id,
            LabInstance.lab_id == lab_id,
            LabInstance.status.in_([LabInstanceStatus.STARTING, LabInstanceStatus.RUNNING])
        ).first()
        
        if existing:
            return existing
        
        # Create DB record
        instance = LabInstance(
            user_id=user_id,
            lab_id=lab_id,
            status=LabInstanceStatus.STARTING
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        
        try:
            # Start Docker Compose stack
            compose_file = lab.compose_file or os.path.join(self.compose_base_path, "docker-compose.yml")
            
            if not os.path.exists(compose_file):
                raise Exception(f"Compose file not found: {compose_file}")
            
            # Run docker-compose up
            result = subprocess.run(
                ["docker", "compose", "-f", compose_file, "up", "-d"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(compose_file)
            )
            
            if result.returncode != 0:
                logger.error(f"Docker Compose failed: {result.stderr}")
                raise Exception(f"Failed to start lab: {result.stderr}")
            
            # Wait a moment for services to start
            time.sleep(3)
            
            # Update instance
            instance.container_id = f"guac_stack_{lab_id}"  # Placeholder for compose project
            instance.status = LabInstanceStatus.RUNNING
            db.commit()
            
            self.running_stacks[lab_id] = True
            logger.info(f"Guacamole lab {lab_id} started for user {user_id}")
            
            return instance
            
        except Exception as e:
            instance.status = LabInstanceStatus.FAILED
            db.commit()
            logger.error(f"Failed to start Guacamole lab: {e}")
            raise e
    
    def stop_lab(self, db: Session, instance_id: int):
        """Stop a Guacamole lab environment"""
        instance = db.query(LabInstance).filter(LabInstance.id == instance_id).first()
        if not instance:
            return
        
        lab = db.query(Lab).filter(Lab.id == instance.lab_id).first()
        if not lab:
            return
        
        try:
            compose_file = lab.compose_file or os.path.join(self.compose_base_path, "docker-compose.yml")
            
            # Run docker-compose down
            result = subprocess.run(
                ["docker", "compose", "-f", compose_file, "down"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(compose_file)
            )
            
            if result.returncode != 0:
                logger.warning(f"Docker Compose down warning: {result.stderr}")
            
            self.running_stacks.pop(lab.id, None)
            
        except Exception as e:
            logger.error(f"Error stopping Guacamole lab: {e}")
        
        instance.status = LabInstanceStatus.STOPPED
        db.commit()
    
    def get_guacamole_url(self, lab: Lab) -> str:
        """Get the Guacamole URL for a lab"""
        if lab.guacamole_url:
            return lab.guacamole_url
        # Default Guacamole URL
        return "http://localhost:8085/guacamole"
    
    def is_running(self, lab_id: int) -> bool:
        """Check if a lab stack is running"""
        return self.running_stacks.get(lab_id, False)


# Singleton instance
guacamole_manager = GuacamoleManager()
