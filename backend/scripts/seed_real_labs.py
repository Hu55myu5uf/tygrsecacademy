
import sys
import os
from sqlalchemy.orm import Session

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.labs import Lab, LabDifficulty
import models.user # Register User model

def seed_labs():
    db = SessionLocal()
    try:
        print("Seeding real labs...")
        
        lab_data = {
            "title": "Network Reconnaissance Environment",
            "description": "Practice network discovery and port scanning techniques using Nmap in a safe, isolated container.",
            "docker_image": "alpine:latest",
            "difficulty": LabDifficulty.BEGINNER,
            "category": "Network Security",
            "estimated_minutes": 45,
            "content": """
# Network Reconnaissance with Nmap

## Introduction
Network reconnaissance is the first step in any penetration testing engagement. In this lab, you will learn how to use **Nmap** (Network Mapper) to discover hosts and services on a network.

## Environment
You are provided with an **Alpine Linux** container pre-installed with `nmap` and `netcat`.

## Objectives
1.  **Verify Nmap Installation**
    - Run `nmap --version` to check the installed version.
2.  **Scan Localhost**
    - Run `nmap localhost` to see open ports on your own container.
3.  **Port Scanning**
    - Use `nc -l -p 8080 &` to listen on port 8080.
    - Run `nmap -p 8080 localhost` to confirm it is discovered.

## Quick Reference
- `nmap -sV <target>`: Service version detection
- `nmap -O <target>`: OS detection
- `nmap -p- <target>`: Scan all 65535 ports

> **Note:** This is an isolated environment. Do not attempt to scan external targets.
"""
        }

        existing = db.query(Lab).filter(Lab.title == lab_data["title"]).first()
        if existing:
            print(f"Updating existing lab: {existing.title}")
            for key, value in lab_data.items():
                setattr(existing, key, value)
        else:
            print(f"Creating new lab: {lab_data['title']}")
            lab = Lab(**lab_data)
            db.add(lab)
        
        db.commit()
        print("Lab seeding complete!")

    except Exception as e:
        print(f"Error seeding labs: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_labs()
