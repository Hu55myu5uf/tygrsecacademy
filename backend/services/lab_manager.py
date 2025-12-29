
import docker
import socket
import time
from typing import Optional, Dict
from sqlalchemy.orm import Session
from models.labs import Lab, LabInstance, LabInstanceStatus

class LabManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Error connecting to Docker Daemon: {e}")
            self.client = None

    def start_lab(self, db: Session, user_id: int, lab_id: int) -> LabInstance:
        """
        Start a new lab instance for a user.
        """
        if not self.client:
            raise Exception("Docker service is not available")
            
        # Get Lab details
        lab = db.query(Lab).filter(Lab.id == lab_id).first()
        if not lab:
            raise Exception(f"Lab {lab_id} not found")

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
            # Start Container
            # Use image from Lab model, default to alpine if not specified
            image_name = lab.docker_image if hasattr(lab, 'docker_image') and lab.docker_image else "alpine:latest"
            
            # Check if image exists locally, pull if not
            try:
                self.client.images.get(image_name)
            except docker.errors.ImageNotFound:
                print(f"Pulling image {image_name}...")
                self.client.images.pull(image_name)

            # Determine command based on image type
            # For full OS images (Kali/Ubuntu), we usually want them to stay alive
            cmd = "tail -f /dev/null" if "alpine" not in image_name else "sh -c 'apk add --no-cache nmap netcat-openbsd && while true; do sleep 1000; done'"
            
            # Override for specific known images if needed
            if "kali" in image_name:
                cmd = "/bin/bash -c 'while true; do sleep 1000; done'"

            container = self.client.containers.run(
                image_name,
                command=cmd,
                detach=True,
                tty=True, # Enable TTY
                stdin_open=True, # Keep stdin open
                name=f"lab_{user_id}_{lab_id}_{int(time.time())}",
                # Limits to prevent abuse
                mem_limit="512m", # Increased for Kali
                cpu_quota=50000,
                # Network isolation would happen here
            )

            # Update DB with container ID
            instance.container_id = container.id
            instance.status = LabInstanceStatus.RUNNING
            db.commit()
            
            return instance

        except Exception as e:
            instance.status = LabInstanceStatus.FAILED
            db.commit()
            print(f"Failed to start container: {e}")
            raise e

    def stop_lab(self, db: Session, instance_id: int):
        instance = db.query(LabInstance).filter(LabInstance.id == instance_id).first()
        if not instance or not instance.container_id:
            return

        if self.client:
            try:
                container = self.client.containers.get(instance.container_id)
                container.stop()
                container.remove()
            except docker.errors.NotFound:
                pass
            except Exception as e:
                print(f"Error stopping container: {e}")

        instance.status = LabInstanceStatus.STOPPED
        db.commit()

    def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        if not self.client:
            return ""
        try:
            container = self.client.containers.get(container_id)
            return container.logs(tail=tail).decode('utf-8')
        except Exception:
            return ""

lab_manager = LabManager()
