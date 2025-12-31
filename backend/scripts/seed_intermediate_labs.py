"""
Seed script for additional intermediate labs
Creates 2 new labs using the existing pentest infrastructure
"""
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.labs import Lab, LabDifficulty, LabType
import models.user

def seed_intermediate_labs():
    db = SessionLocal()
    try:
        print("Seeding additional intermediate labs...")
        
        # Lab 1: OWASP Juice Shop
        juice_shop_lab = {
            "title": "OWASP Juice Shop Challenges",
            "description": "Exploit a modern vulnerable web application. Practice XSS, SQL injection, broken authentication, and more using OWASP's flagship training app.",
            "docker_image": "bkimminich/juice-shop:latest",
            "difficulty": LabDifficulty.INTERMEDIATE,
            "category": "Web Security",
            "estimated_minutes": 90,
            "lab_type": LabType.GUACAMOLE,  # Using guacamole type for iframe-based labs
            "guacamole_url": "http://localhost:8087",  # Direct Juice Shop URL
            "compose_file": os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "docker", "juice-shop", "docker-compose.yml"
            )),
            "content": """
# OWASP Juice Shop Challenges

## Introduction
OWASP Juice Shop is the most modern and sophisticated insecure web application. It contains over **100 security challenges** of varying difficulty.

## Getting Started
1. After starting the lab, Juice Shop opens in an iframe
2. Explore the application - it's a fake e-commerce site
3. Access the **Score Board** at `/score-board` to track challenges

## Challenge Categories

### 1. Injection Attacks ⭐⭐
**Challenge:** Login as admin without knowing the password

Try these in the login form:
```
Email: ' or 1=1--
Password: anything
```

Or use the email field:
```
admin@juice-sh.op'--
```

### 2. Broken Access Control ⭐⭐
**Challenge:** Access another user's shopping basket

1. Login as any user
2. Open browser DevTools (F12) → Network tab
3. Look for basket API calls
4. Try changing the basket ID in the URL

### 3. XSS (Cross-Site Scripting) ⭐
**Challenge:** Perform a DOM XSS attack

1. Go to the search bar
2. Try: `<iframe src="javascript:alert('xss')">`
3. Check the Score Board to verify

### 4. Sensitive Data Exposure ⭐
**Challenge:** Find the hidden Score Board

Hint: Try accessing `/score-board` directly or search the page source.

### 5. Broken Authentication ⭐⭐⭐
**Challenge:** Reset Jim's password

1. Go to Forgot Password
2. Enter Jim's email: `jim@juice-sh.op`
3. Find the security question answer (Star Trek reference!)

## Tools to Use
- **Browser DevTools** (F12) - Inspect network traffic and DOM
- **Burp Suite** (if installed) - Intercept and modify requests

## Scoring
Access the Score Board at `/score-board` to track your progress!

> **Tip:** Click the light bulb icon for hints on each challenge.
"""
        }

        # Lab 2: OWASP WebGoat
        webgoat_lab = {
            "title": "OWASP WebGoat Security Training",
            "description": "Learn web security through guided lessons. WebGoat teaches you about vulnerabilities with interactive exercises and hints.",
            "docker_image": "webgoat/webgoat:latest",
            "difficulty": LabDifficulty.INTERMEDIATE,
            "category": "Web Security",
            "estimated_minutes": 75,
            "lab_type": LabType.GUACAMOLE,  # Using guacamole type for browser-based labs
            "guacamole_url": "http://localhost:8088/WebGoat",  # WebGoat URL
            "compose_file": os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "docker", "bwapp", "docker-compose.yml"
            )),
            "content": """
# OWASP WebGoat Security Training

## Introduction
WebGoat is a deliberately insecure web application maintained by OWASP. It's designed to teach web security concepts through interactive lessons.

## Getting Started
1. After starting the lab, WebGoat opens in a new tab
2. Click **Register new user** to create an account
3. Login and start the lessons!

## Lesson Categories

### A1: Injection ⭐⭐
Learn about SQL injection, path traversal, and more:
- **SQL Injection (intro)** - Basic SQL injection concepts
- **SQL Injection (advanced)** - Union attacks, blind injection
- **Path Traversal** - Access files outside web root

### A2: Broken Authentication ⭐⭐
- **Authentication Bypasses** - Exploit weak auth mechanisms
- **JWT Tokens** - Crack and forge JWT tokens
- **Password Reset** - Abuse password reset flows

### A3: Sensitive Data Exposure ⭐
- **Insecure Login** - Find credentials in transit
- **Crypto Basics** - Understand encryption weaknesses

### A5: Broken Access Control ⭐⭐
- **Insecure Direct Object References** - Access other users' data
- **Missing Function Level Access Control** - Access admin functions

### A7: Cross-Site Scripting (XSS) ⭐⭐
- **Reflected XSS** - Inject scripts via URL
- **Stored XSS** - Persist malicious scripts
- **DOM-based XSS** - Client-side vulnerabilities

### A8: Insecure Deserialization ⭐⭐⭐
- Learn how to exploit Java deserialization

### A10: Insufficient Logging ⭐
- Understand why logging matters for security

## Tips
- Each lesson has **hints** - click the lightbulb icon
- Solutions are available if you get stuck
- Complete lessons to earn points!

## Tools to Use
- **Browser DevTools** (F12) - Inspect requests
- **Burp Suite** - Intercept and modify traffic

> **Tip:** WebGoat teaches concepts progressively. Start from the beginning!
"""
        }

        # Insert/Update labs
        for lab_data in [juice_shop_lab, webgoat_lab]:
            existing = db.query(Lab).filter(Lab.title == lab_data["title"]).first()
            if existing:
                print(f"Updating: {existing.title}")
                for key, value in lab_data.items():
                    setattr(existing, key, value)
            else:
                print(f"Creating: {lab_data['title']}")
                lab = Lab(**lab_data)
                db.add(lab)
        
        db.commit()
        print("\n✅ Intermediate labs seeded successfully!")
        print("\nLabs added/updated:")
        print("  1. OWASP Juice Shop Challenges")
        print("  2. OWASP WebGoat Security Training")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_intermediate_labs()
