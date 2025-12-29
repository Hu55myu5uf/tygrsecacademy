"""
Seed sample capstone tier projects
Run this to populate the database with capstone project templates for Tiers 1-3
"""
from database.connection import get_db
from models.capstone import CapstoneTier
from models.curriculum import Tier
import models.user
import models.progress
import models.challenge
import models.lab

def seed_capstone_tiers():
    db = next(get_db())
    
    try:
        # Check if capstones already exist
        existing = db.query(CapstoneTier).first()
        if existing:
            print("❌ Capstone tiers already exist. Skipping seed.")
            return
        
        # Get tiers
        tiers = db.query(Tier).order_by(Tier.order).all()
        
        if not tiers or len(tiers) < 3:
            print("❌ Please seed tiers first!")
            return
        
        print("Creating capstone tier projects...")
        
        # Tier 1 Capstone
        tier1_capstone = CapstoneTier(
            tier_id=tiers[0].id,
            title="Personal Portfolio Website with Security Features",
            description="Build a professional portfolio website demonstrating secure web development practices learned in Tier 1.",
            requirements="""
## Requirements

Your portfolio website must include:

1. **Security Features**
   - HTTPS implementation
   - Secure headers (CSP, X-Frame-Options, etc.)
   - Input validation and sanitization
   - Protection against common vulnerabilities (XSS, CSRF)

2. **Content**
   - About Me section
   - Projects showcase
   - Contact form with proper validation
   - Responsive design

3. **Technical Implementation**
   - Clean, semantic HTML5
   - CSS with modern features
   - Vanilla JavaScript or a framework
   - Git version control

4. **Documentation**
   - README with setup instructions
   - Security features documentation
   - Deployment guide
            """,
            deliverables=[
                "GitHub repository with source code",
                "Live deployed website URL",
                "Security documentation (500-1000 words)",
                "Demo video (3-5 minutes)"
            ],
            rubric={
                "criteria": [
                    {
                        "name": "Security Implementation",
                        "description": "Proper implementation of security best practices",
                        "max_points": 30
                    },
                    {
                        "name": "Code Quality",
                        "description": "Clean, well-organized, and documented code",
                        "max_points": 25
                    },
                    {
                        "name": "Functionality",
                        "description": "All required features working correctly",
                        "max_points": 25
                    },
                    {
                        "name": "Documentation",
                        "description": "Clear documentation and write-up",
                        "max_points": 20
                    }
                ]
            },
            max_score=100,
            passing_score=70
        )
        
        # Tier 2 Capstone
        tier2_capstone = CapstoneTier(
            tier_id=tiers[1].id,
            title="Vulnerable Web Application & Penetration Test Report",
            description="Create an intentionally vulnerable web application and perform a comprehensive penetration test on it.",
            requirements="""
## Requirements

1. **Vulnerable Application**
   - Build a web app with 5-10 intentional vulnerabilities
   - Include OWASP Top 10 vulnerabilities
   - Provide source code

2. **Penetration Testing**
   - Perform thorough security testing
   - Document all findings
   - Provide remediation recommendations

3. **Report**
   - Executive summary
   - Detailed findings with CVSS scores
   - Proof-of-concept exploits
   - Remediation strategies
   - Lessons learned

4. **Demonstration**
   - Video demonstrating vulnerabilities
   - Live exploitation examples
            """,
            deliverables=[
                "Vulnerable application source code (GitHub)",
                "Penetration test report (PDF, 10-20 pages)",
                "Proof-of-concept exploits",
                "Demo video (10-15 minutes)"
            ],
            rubric={
                "criteria": [
                    {
                        "name": "Vulnerability Implementation",
                        "description": "Realistic and diverse vulnerabilities",
                        "max_points": 25
                    },
                    {
                        "name": "Penetration Testing",
                        "description": "Thorough testing methodology",
                        "max_points": 25
                    },
                    {
                        "name": "Report Quality",
                        "description": "Professional, detailed report",
                        "max_points": 30
                    },
                    {
                        "name": "Remediation Guidance",
                        "description": "Clear and actionable remediation steps",
                        "max_points": 20
                    }
                ]
            },
            max_score=100,
            passing_score=75
        )
        
        # Tier 3 Capstone
        tier3_capstone = CapstoneTier(
            tier_id=tiers[2].id,
            title="CTF Platform - Design & Implementation",
            description="Design and build a mini Capture The Flag (CTF) platform with custom challenges.",
            requirements="""
## Requirements

1. **Platform Features**
   - User registration and authentication
   - Challenge categories (Web, Crypto, Reverse Engineering, etc.)
   - Scoring system
   - Leaderboard
   - Admin panel for challenge management

2. **Custom Challenges**
   - Create 5-10 original CTF challenges
   - Multiple difficulty levels
   - Hints system
   - Dynamic flag generation

3. **Security**
   - Secure authentication
   - Protection against common attacks
   - Rate limiting
   - Input validation

4. **Documentation**
   - Architecture overview
   - Setup and deployment guide
   - Challenge write-ups
   - API documentation

5. **Deployment**
   - Deployed and accessible online
   - Scalable architecture
            """,
            deliverables=[
                "Full platform source code (GitHub)",
                "Live deployed platform URL",
                "Technical documentation (15-25 pages)",
                "Challenge write-ups",
                "Demo video (15-20 minutes)"
            ],
            rubric={
                "criteria": [
                    {
                        "name": "Platform Functionality",
                        "description": "Complete working CTF platform",
                        "max_points": 30
                    },
                    {
                        "name": "Challenge Quality",
                        "description": "Original, well-designed challenges",
                        "max_points": 25
                    },
                    {
                        "name": "Security Implementation",
                        "description": "Secure platform architecture",
                        "max_points": 25
                    },
                    {
                        "name": "Documentation & Presentation",
                        "description": "Comprehensive docs and demo",
                        "max_points": 20
                    }
                ]
            },
            max_score=100,
            passing_score=75
        )
        
        db.add(tier1_capstone)
        db.add(tier2_capstone)
        db.add(tier3_capstone)
        db.commit()
        
        print("✅ Successfully created 3 capstone tier projects!")
        print(f"  - Tier 1: {tier1_capstone.title}")
        print(f"  - Tier 2: {tier2_capstone.title}")
        print(f"  - Tier 3: {tier3_capstone.title}")
        
    except Exception as e:
        print(f"❌ Error seeding capstone tiers: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_capstone_tiers()
