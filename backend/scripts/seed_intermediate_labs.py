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
            "lab_type": LabType.GUACAMOLE,
            "guacamole_url": "http://localhost:8085/guacamole",
            "compose_file": os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "docker", "pentest-lab", "docker-compose.yml"
            )),
            "content": """
# OWASP Juice Shop Challenges

## Introduction
OWASP Juice Shop is the most modern and sophisticated insecure web application. It contains over **100 security challenges** of varying difficulty.

## Environment
- **Kali Linux** - Attack machine via VNC
- **Juice Shop** - Target at `http://pentest_juice_shop:3000`

## Access via Guacamole
1. Login: `tygr` / `tygrsec123`
2. Click **"Kali Attack Machine"**
3. Open Firefox: `firefox http://pentest_juice_shop:3000`

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

Hint: Try accessing `/score-board` directly or search the page source for clues.

### 5. Broken Authentication ⭐⭐⭐
**Challenge:** Reset Jim's password

1. Go to Forgot Password
2. Enter Jim's email: `jim@juice-sh.op`
3. Find the security question answer (check Star Trek references!)

## Tools to Use
- **Burp Suite** - Intercept and modify requests
- **Browser DevTools** - Inspect network traffic and DOM
- **SQLMap** - Automated SQL injection

## Scoring
Access the Score Board at `/score-board` to track your progress!

> **Tip:** The Juice Shop has a built-in tutorial for each challenge. Click the light bulb icon for hints.
"""
        }

        # Lab 2: Network Reconnaissance & Enumeration
        network_recon_lab = {
            "title": "Network Reconnaissance & Enumeration",
            "description": "Master network scanning and service enumeration techniques. Discover hosts, identify services, and map network topology using professional tools.",
            "docker_image": "kalilinux/kali-rolling",
            "difficulty": LabDifficulty.INTERMEDIATE,
            "category": "Network Security",
            "estimated_minutes": 75,
            "lab_type": LabType.GUACAMOLE,
            "guacamole_url": "http://localhost:8085/guacamole",
            "compose_file": os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "docker", "pentest-lab", "docker-compose.yml"
            )),
            "content": """
# Network Reconnaissance & Enumeration

## Introduction
Network reconnaissance is the foundation of penetration testing. This lab teaches you to discover and analyze network targets using professional tools.

## Environment
- **Kali Linux** - Attack machine via VNC
- **Target Network** - 172.28.0.0/16
  - pentest_dvwa (Web Server)
  - pentest_juice_shop (Node.js App)
  - pentest_vulnerable_ssh (SSH Server)
  - pentest_dvwa_db (MySQL Database)

## Access via Guacamole
Login: `tygr` / `tygrsec123` → Click "Kali Attack Machine"

## Exercises

### Exercise 1: Host Discovery
Find all live hosts on the network:

```bash
# Ping scan (fast)
nmap -sn 172.28.0.0/24

# ARP scan (more reliable in local networks)
nmap -PR 172.28.0.0/24
```

**Expected Result:** 5-6 hosts discovered

### Exercise 2: Port Scanning
Identify open ports on discovered hosts:

```bash
# Quick scan (top 1000 ports)
nmap 172.28.0.0/24

# Full port scan (all 65535 ports)
nmap -p- pentest_dvwa

# Specific port range
nmap -p 1-1000,3000,3306 172.28.0.0/24
```

### Exercise 3: Service Version Detection
Identify software versions running on open ports:

```bash
# Service version detection
nmap -sV pentest_dvwa pentest_juice_shop pentest_vulnerable_ssh

# Aggressive scan (includes OS detection)
nmap -A pentest_dvwa
```

**Document the versions found:**
- What web server is DVWA running?
- What version of SSH is vulnerable-ssh running?

### Exercise 4: OS Detection
Fingerprint the operating systems:

```bash
nmap -O pentest_dvwa
nmap -O --osscan-guess 172.28.0.0/24
```

### Exercise 5: Script Scanning
Use Nmap scripts for deeper enumeration:

```bash
# Default scripts
nmap -sC pentest_dvwa

# HTTP enumeration
nmap --script http-enum pentest_dvwa

# SSH enumeration
nmap --script ssh-auth-methods pentest_vulnerable_ssh

# Vulnerability scan
nmap --script vuln pentest_dvwa
```

### Exercise 6: Create a Network Map
Document your findings:

| Host | IP | Open Ports | Services |
|------|-----|------------|----------|
| DVWA | ? | ? | ? |
| Juice Shop | ? | ? | ? |
| SSH Server | ? | ? | ? |
| Database | ? | ? | ? |

## Advanced Techniques

### Stealth Scanning
```bash
# SYN scan (stealthier)
nmap -sS pentest_dvwa

# Timing control (slower = stealthier)
nmap -T2 pentest_dvwa
```

### Save Results
```bash
# Output to all formats
nmap -oA scan_results 172.28.0.0/24

# XML output for tools
nmap -oX results.xml 172.28.0.0/24
```

## Summary
By completing this lab, you should be able to:
- ✅ Discover live hosts on a network
- ✅ Identify open ports and services
- ✅ Determine software versions
- ✅ Document network topology
"""
        }

        # Insert/Update labs
        for lab_data in [juice_shop_lab, network_recon_lab]:
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
        print("\nNew labs added:")
        print("  1. OWASP Juice Shop Challenges")
        print("  2. Network Reconnaissance & Enumeration")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_intermediate_labs()
