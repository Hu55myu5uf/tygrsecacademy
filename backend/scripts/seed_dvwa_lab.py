"""
Seed script for DVWA Lab (Lightweight - Browser Access)
Creates a lab entry that uses direct browser access to DVWA
"""
import sys
import os
from sqlalchemy.orm import Session

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.labs import Lab, LabDifficulty, LabType
import models.user  # Register User model

def seed_dvwa_lab():
    db = SessionLocal()
    try:
        print("Seeding DVWA Browser lab (lightweight)...")
        
        lab_data = {
            "title": "Web Application Penetration Testing",
            "description": "Attack a vulnerable web application (DVWA) directly in your browser. Practice SQL injection, XSS, and more in a safe environment.",
            "docker_image": "vulnerables/web-dvwa:latest",
            "difficulty": LabDifficulty.INTERMEDIATE,
            "category": "Web Security",
            "estimated_minutes": 60,
            "lab_type": LabType.GUACAMOLE,  # Using guacamole type for iframe-based labs
            "guacamole_url": "http://localhost:8086",  # Direct DVWA URL
            "compose_file": os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "docker", "guacamole", "docker-compose.yml"
            )),
            "content": """
# Web Application Penetration Testing with DVWA

## Introduction
In this lab, you will practice attacking a **Damn Vulnerable Web Application (DVWA)** directly in your browser.

## Environment
- **DVWA Web Application** - Accessible at `http://localhost:8086`
- **Your Browser Tools** - Use DevTools (F12), Burp Suite, or browser extensions

## DVWA Setup
1. After starting the lab, DVWA opens in an iframe
2. Login with: **admin** / **password**
3. Go to **DVWA Security** → Set to **Low**
4. Click **Create / Reset Database** (first time only)

## Objectives

### 1. SQL Injection
Navigate to **SQL Injection** and try:
```sql
1' OR '1'='1
```

### 2. Command Injection
Navigate to **Command Injection** and try:
```
127.0.0.1; cat /etc/passwd
```

### 3. XSS (Reflected)
Navigate to **XSS (Reflected)** and try:
```html
<script>alert('XSS')</script>
```

### 4. File Inclusion
Navigate to **File Inclusion** and try:
```
?page=../../../etc/passwd
```

### 5. Brute Force
Navigate to **Brute Force** and use username `admin` with common passwords

## Tools You Can Use
- **Browser DevTools** (F12) - Inspect network traffic
- **Burp Suite** (if installed) - Intercept and modify requests
- **SQLMap** - Automated SQL injection
- **curl** - Command-line HTTP requests

## Security Levels
DVWA has 4 security levels:
- **Low** - No security (learning mode)
- **Medium** - Some protection
- **High** - Strong protection
- **Impossible** - Secure code example

Start with **Low** and work your way up!

> **Note:** This is an isolated environment. DVWA runs in a Docker container.
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
        print("DVWA lab seeded successfully!")
        print(f"\nTo start the lab infrastructure, run:")
        print(f"  cd docker/guacamole")
        print(f"  docker compose up -d")
        print(f"\nThen access DVWA at: http://localhost:8086")

    except Exception as e:
        print(f"Error seeding lab: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_dvwa_lab()
