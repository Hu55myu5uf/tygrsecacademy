"""
Seed Tiers 3 & 4 - All lessons
Tier 3: CTF Challenges (~24 lessons)
Tier 4: Mastery & Publishing (~18 lessons)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def cl(db, mid, o, t, d, m, c):
    """Create lesson helper"""
    ex = db.query(Lesson).filter(Lesson.module_id == mid, Lesson.order == o).first()
    if not ex:
        l = Lesson(module_id=mid, order=o, title=t, description=d, duration_minutes=m, content_markdown=c, is_published=True)
        db.add(l)
        print(f"  ✅ {o}. {t}")
    else:
        ex.title, ex.description, ex.duration_minutes, ex.content_markdown, ex.is_published = t, d, m, c, True
        print(f"  ✅ {o}. {t}")

db = SessionLocal()

print("🚀 Seeding Tiers 3 & 4")
print("=" * 60)

m11 = db.query(Module).filter(Module.title == "OSINT Challenges").first()
m12 = db.query(Module).filter(Module.title == "Malware Analysis CTF").first()
m13 = db.query(Module).filter(Module.title == "Adversarial ML Challenges").first()
m14 = db.query(Module).filter(Module.title == "Competitive Challenges").first()
m15 = db.query(Module).filter(Module.title == "Capstone Projects").first()
m16 = db.query(Module).filter(Module.title == "Tutor Supervision").first()
m17 = db.query(Module).filter(Module.title == "Security Blogging").first()

if not all([m11, m12, m13, m14, m15, m16, m17]):
    print("❌ Modules not found!")
    db.close()
    exit(1)

# TIER 3: CTF CHALLENGES
print("\n🏆 Module 11: OSINT Challenges (6 lessons)")

cl(db, m11.id, 1, "Social Media OSINT", "Track targets through social media platforms", 45, """# Social Media OSINT

## Challenge: Find the Target
Using only a username, locate the target's:
- Full name
- Location
- Organization
- Associates

## Tools
- Sherlock
- Social-Analyzer
- Holehe

## Scoring
- Name: 20 pts
- Location: 30 pts  
- Workplace: 30 pts
- Associates: 20 pts

**Flag format**: `TYGR{name_city_company}`
""")

cl(db, m11.id, 2, "Domain Reconnaissance CTF", "Comprehensive domain intelligence gathering", 50, """# Domain Recon CTF

## Objective
Given a domain, find:
- Subdomains
- Email addresses
- Technologies used
- S3 buckets
- GitHub repos

## Tools & Techniques
- Amass, Sublist3r
- theHarvester
- Wappalyzer
- Google Dorking

**Points**: 100 total (20 per finding)
""")

cl(db, m11.id, 3, "Geolocation Challenge", "Pin point exact locations from images", 50, """# Geolocation CTF

## Challenge
Given photos, determine exact coordinates

## Techniques
- EXIF data analysis
- Landmark recognition
- Shadow analysis
- Reverse image search

## Scoring
- Within 1km: 100 pts
- Within 10km: 50 pts
- City correct: 25 pts
""")

cl(db, m11.id, 4, "Email Investigation", "Trace email origins and find sender info", 45, """# Email OSINT

## Task
Analyze suspicious email headers to find:
- Sender's real IP
- Email server path
- Geolocation
- Organization

## Tools
- Email Header Analyzer
- MXToolbox
- IP Geolocation

**Flag**: Real sender IP address
""")

cl(db, m11.id, 5, "Digital Footprint Analysis", "Complete profile from minimal information", 60, """# Digital Footprint CTF

## Challenge
Build complete dossier from:
- Phone number OR
- Email address OR  
- Username

## Required Intel
- Social profiles
- Addresses
- Associates
- Interests
- Work history

**Scoring**: Comprehensive report (200 pts max)
""")

cl(db, m11.id, 6, "OSINT CTF Competition", "Timed competitive OSINT challenge", 90, """# Competitive OSINT

## Format
- 90-minute timed challenge
- Multiple targets
- Progressive difficulty
- Leaderboard ranked

## Categories
- Social media (25%)
- Domain recon (25%)
- Geolocation (25%)
- Email tracing (25%)

**Top 3**: Bonus points + certificates
""")

print("\n🦠 Module 12: Malware Analysis CTF (6 lessons)")

cl(db, m12.id, 1, "Static Analysis Challenge", "Analyze malware without execution", 60, """# Static Analysis CTF

## Challenge
Analyze provided malware sample:
- File type and packer
- Embedded strings
- IOCs
- Capabilities

## Tools
- IDA Free
- Ghidra
- PEStudio
- strings, hexdump

**Submission**: IOC list + capability report
""")

cl(db, m12.id, 2, "Reverse Engineering CTF", "Reverse engineer to find the flag", 75, """# Reversing Challenge

## Objective  
Reverse engineer binary to extract:
- Encryption algorithm
- Decryption key
- Hidden flag

## Difficulty Levels
- Easy: Basic XOR
- Medium: Custom cipher
- Hard: Packed + obfuscated

**Points**: 50-200 based on difficulty
""")

cl(db, m12.id, 3, "Malware Behavior Analysis", "Analyze malware in sandbox", 60, """# Dynamic Analysis CTF

## Task
Execute in sandbox and document:
- Network connections
- File system changes
- Registry modifications
- Process injection

## Tools
- Cuckoo Sandbox
- Process Monitor
- Wireshark
- RegShot

**Flag**: C2 domain + persistence mechanism
""")

cl(db, m12.id, 4, "Ransomware Decryption", "Decrypt files and recover data", 90, """# Ransomware Recovery CTF

## Scenario
Files encrypted by custom ransomware

## Challenge
- Reverse malware
- Find crypto weakness
- Write decryptor
- Recover files

**Success Criteria**: Decrypt all files
**Bonus**: Identify ransomware family
""")

cl(db, m12.id, 5, "Exploit Development", "Develop working exploit", 120, """# Exploit Dev Challenge

## Target
Vulnerable application provided

## Objective
- Find vulnerability
- Write exploit
- Achieve code execution
- Capture flag

## Tools
- GDB/WinDbg
- Metasploit
- Python/Perl
- ROPgadget

**Scoring**: Working exploit = 300 pts
""")

cl(db, m12.id, 6, "Malware CTF Championship", "Ultimate malware analysis competition", 120, """# Malware CTF Finals

## Format
- 2-hour competition
- Multiple samples
- Various difficulty levels
- Team or individual

## Categories
- Static analysis
- Dynamic analysis
- Reverse engineering
- Exploit development

**Prizes**: Top performers get recognition + rewards
""")

print("\n🤖 Module 13: Adversarial ML Challenges (6 lessons)")

cl(db, m13.id, 1, "Model Evasion Challenge", "Bypass ML detection models", 60, """# ML Evasion CTF

## Objective
Craft inputs that:
- Are clearly malicious
- Evade ML detector
- Maintain functionality

## Scenarios
- Spam filter bypass
- Malware detector evasion
- Face recognition bypass

**Scoring**: Evasion rate × confidence
""")

cl(db, m13.id, 2, "Data Poisoning Attack", "Poison training data to backdoor model", 75, """# Data Poisoning CTF

## Challenge
Inject malicious samples into training set to:
- Create backdoor
- Reduce accuracy on specific inputs
- Remain undetected

## Metrics
- Success rate of backdoor
- Model accuracy retained
- Detection evasion

**Points**: Based on stealth + effectiveness
""")

cl(db, m13.id, 3, "Model Extraction Attack", "Steal ML model via queries", 60, """# Model Theft CTF

## Task
Extract model from black-box API:
- Query budget: 10,000
- Goal: Replicate model behavior
- Accuracy target: \u003e90%

## Techniques
- Query optimization
- Active learning
- Transfer learning

**Success**: Stolen model accuracy
""")

cl(db, m13.id, 4, "Adversarial Examples", "Generate adversarial inputs", 60, """# Adversarial Generation CTF

## Challenge
Create adversarial examples for:
- Image classifier
- Text classifier
- Network IDS

## Constraints
- L∞ norm \u003c 0.1
- Semantic preservation
- Transferability

**Scoring**: Attack success rate
""")

cl(db, m13.id, 5, "Robust Model Challenge", "Build defenses against adversarial attacks", 90, """# ML Defense CTF

## Objective
Harden ML model against:
- Evasion attacks
- Poisoning
- Model extraction

## Defenses
- Adversarial training
- Input validation
- Model ensemble
- Detection mechanisms

**Competition**: Attack vs Defense teams
""")

cl(db, m13.id, 6, "AI Red Team Competition", "Comprehensive ML attack challenge", 120, """# AI Security CTF Finals

## Format
- Attack multiple ML systems
- Various attack vectors
- Point-based scoring
- Leaderboard

## Targets
- IDS models
- Fraud detection
- Biometric auth
- Content moderation

**Awards**: Top red teams recognized
""")

print("\n🏅 Module 14: Competitive Challenges (6 lessons)")

cl(db, m14.id, 1, "Speed Hacking Challenge", "Fastest to root wins", 30, """# Speed Challenge

## Format
- Pre-configured vulnerable machine
- First to root wins
- Time-based scoring

## Rules
- Submit proof (flag)
- Fastest time wins
- Must document method

**Prizes**: 1st: 500pts, 2nd: 300pts, 3rd: 100pts
""")

cl(db, m14.id, 2, "King of the Hill", "Maintain control of the server", 60, """# King of the Hill

## Objective
- Compromise server
- Maintain access
- Kick out others
- Fix vulnerabilities

## Scoring
- Control time = points
- Longer control = more points
- Must defend while attacking

**Duration**: 60 minutes
""")

cl(db, m14.id, 3, "Attack-Defense CTF", "Attack others, defend yourself", 90, """# Attack-Defense

## Format
- Each team has identical vulnerable server
- Attack opponents
- Defend your own
- Capture flags from others

## Scoring
- Offense: Flags captured
- Defense: Uptime + patches
- Combined score

**Teams**: 4-6 members recommended
""")

cl(db, m14.id, 4, "Jeopardy-Style CTF", "Multi-category challenge board", 120, """# Jeopardy CTF

## Categories
- Web (100-500pts)
- Crypto (100-500pts)
- Reversing (100-500pts)
- Forensics (100-500pts)
- OSINT (100-500pts)

## Format
- Choose challenges
- Progressive difficulty
- Hints cost points
- First blood bonus

**Duration**: 2 hours
""")

cl(db, m14.id, 5, "Team Tournament", "Collaborative team competition", 180, """# Team CTF Tournament

## Structure
- Teams of 3-5
- Round-robin matches
- Mixed challenges
- Playoffs for top 4

## Challenges
- Technical skills
- Teamwork
- Time management
- Strategy

**Prize Pool**: Points distributed to top 3 teams
""")

cl(db, m14.id, 6, "Championship Finals", "Ultimate skill competition", 240, """# TygrSec Championship

## Grand Finals
- Top performers from all modules
- High-stakes challenges
- Live leaderboard
- Spectator mode

## Format
- 4-hour marathon
- 50+ challenges
- Surprise categories
- Dynamic scoring

**Recognition**: Hall of Fame + Certificates
**Rewards**: Top 10 get special badges
""")

# TIER 4: MASTERY & PUBLISHING
print("\n🎯 Module 15: Capstone Projects (6 lessons)")

cl(db, m15.id, 1, "Project Planning & Proposal", "Design your capstone security project", 60, """# Capstone Planning

## Requirements
Select from:
- Build security tool
- Research project
- Enterprise assessment
- CTF platform
- Open source contribution

## Proposal Must Include
- Problem statement
- Objectives
- Methodology
- Timeline
- Expected outcomes

**Deliverable**: Approved project proposal
""")

cl(db, m15.id, 2, "Research & Development", "Execute your project phase 1", 120, """# R&D Phase

## Activities
- Literature review
- Technology selection
- Proof of concept
- Initial implementation

## Milestones
- Week 1: Research complete
- Week 2: PoC working
- Week 3: Core features
- Week 4: Alpha version

**Documentation**: Progress reports
""")

cl(db, m15.id, 3, "Implementation & Testing", "Build and validate your project", 180, """# Implementation

## Deliverables
- Working prototype
- Test suite
- Documentation
- User guide

## Quality Criteria
- Functionality
- Security
- Performance
- Usability

**Review**: Tutor checkpoint
""")

cl(db, m15.id, 4, "Security Assessment", "Test and harden your project", 120, """# Security Validation

## Testing
- Vulnerability assessment
- Penetration testing
- Code review
- Threat modeling

## Tools
- Static analysis
- Dynamic testing
- Fuzzing
- Manual review

**Goal**: Production-ready security
""")

cl(db, m15.id, 5, "Documentation & Presentation", "Professional project documentation", 90, """# Project Documentation

## Components
- Technical documentation
- Architecture diagrams
- User manual
- Security analysis
- Lessons learned

## Presentation
- 20-minute demo
- Q&A session
- Peer review

**Format**: Professional report + slides
""")

cl(db, m15.id, 6, "Final Defense & Deployment", "Present and deploy your capstone", 120, """# Final Defense

## Presentation
- Demonstrate project
- Explain technical decisions
- Discuss challenges
- Future improvements

## Deployment
- Production deployment OR
- Open source release OR
- Research publication

**Evaluation**: Tutor panel review
**Certification**: Capstone completion certificate
""")

print("\n👨‍🏫 Module 16: Tutor Supervision (6 lessons)")

cl(db, m16.id, 1, "One-on-One Mentorship Sessions", "Personalized guidance from experts", 60, """# Mentorship Program

## Format
- Weekly 1-on-1 sessions
- 60 minutes each
- Video or in-person

## Topics
- Career guidance
- Technical deep-dives
- Project review
- Skill assessment

**Scheduling**: Book via platform
""")

cl(db, m16.id, 2, "Code Review Sessions", "Expert review of your code", 60, """# Professional Code Review

## Process
1. Submit code for review
2. Tutor analyzes
3. Review session
4. Refactor together

## Focus Areas
- Security best practices
- Code quality
- Performance
- Maintainability

**Frequency**: Bi-weekly
""")

cl(db, m16.id, 3, "Career Development Planning", "Chart your security career path", 60, """# Career Roadmap

## Activities
- Skills assessment
- Goal setting
- Industry insights
- Job market analysis

## Deliverables
- Career plan
- Learning objectives
- Timeline
- Action items

**Tutor**: Industry professional
""")

cl(db, m16.id, 4, "Resume & Portfolio Building", "Create compelling professional materials", 60, """# Professional Branding

## Components
- Technical resume
- GitHub portfolio
- LinkedIn optimization
- Personal website

## Review
- Tutor feedback
- Industry alignment
- ATS optimization

**Output**: Job-ready materials
""")

cl(db, m16.id, 5, "Mock Interviews", "Practice technical interviews", 90, """# Interview Preparation

## Format
- Technical questions
- Coding challenges
- System design
- Behavioral questions

## Focus
- SOC Analyst
- Pentester
- Security Engineer
- Roles of choice

**Practice**: Multiple rounds with feedback
""")

cl(db, m16.id, 6, "Industry Connections", "Network with security professionals", 60, """# Professional Networking

## Opportunities
- Guest speaker sessions
- Industry meetups
- Conference preparation
- Job referrals

## Activities
- LinkedIn networking
- Security community engagement
- Conference attendance
- Contribution to open source

**Goal**: Build professional network
""")

print("\n📝 Module 17: Security Blogging (6 lessons)")

cl(db, m17.id, 1, "Technical Writing Fundamentals", "Learn to write effective security content", 60, """# Technical Writing

## Principles
- Clarity
- Accuracy
- Audience awareness
- Structure

## Content Types
- Tutorials
- Walkthroughs
- Research findings
- Tool reviews
- CTF writeups

**Practice**: Write first blog outline
""")

cl(db, m17.id, 2, "Blog Setup & Platform Selection", "Create your security blog", 60, """# Blog Platform

## Options
- Medium
- Dev.to
- Ghost
- Jekyll/Hugo (GitHub Pages)
- WordPress

## Setup
- Domain name
- Hosting
- Theme customization
- Analytics

**Deliverable**: Live blog
""")

cl(db, m17.id, 3, "CTF Writeups & Walkthroughs", "Document your challenges", 90, """# Writeup Creation

## Structure
1. Challenge overview
2. Reconnaisance
3. Exploitation
4. Flag capture
5. Lessons learned

## Best Practices
- Screenshots
- Code snippets
- Explanations
- Reproducible steps

**Publish**: 3 quality writeups
""")

cl(db, m17.id, 4, "Tool Reviews & Tutorials", "Create educational content", 90, """# Educational Content

## Tutorial Topics
- Tool usage guides
- Technique demonstrations
- Automation scripts
- Tool comparisons

## Format
- Introduction
- Step-by-step guide
- Examples
- Conclusion

**Goal**: Help others learn
""")

cl(db, m17.id, 5, "SEO & Audience Building", "Grow your blog readership", 60, """# Blog Growth

## SEO Basics
- Keywords
- Meta descriptions
- Internal linking
- Image optimization

## Promotion
- Social media
- Reddit/forums
- LinkedIn
- Security communities

**Metrics**: Track views, engagement
""")

cl(db, m17.id, 6, "Building Your Brand", "Establish yourself as an expert", 60, """# Personal Branding

## Components
- Consistent publishing
- Social media presence
- Community engagement
- Conference talks
- Podcast appearances

## Long-term
- Build following
- Establish expertise
- Job opportunities
- Speaking engagements

**Success**: Recognized security professional
""")

db.commit()
db.close()

print("\n" + "=" * 60)
print("✅ TIERS 3 & 4 COMPLETE!")
print("   🏆 OSINT Challenges: 6 lessons")
print("   🦠 Malware Analysis CTF: 6 lessons")
print("   🤖 Adversarial ML: 6 lessons")
print("   🏅 Competitive Challenges: 6 lessons")
print("   🎯 Capstone Projects: 6 lessons")
print("   👨‍🏫 Tutor Supervision: 6 lessons")
print("   📝 Security Blogging: 6 lessons")
print("   🎯 Total: 42 lessons")
print("\n🎉 COMPLETE CURRICULUM: 130 LESSONS!")
