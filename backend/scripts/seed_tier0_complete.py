import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson

def seed_tier0_remaining_modules(db: Session):
    """Seed Python and AI/ML modules for Tier 0"""
    print("Seeding Python for Security and AI/ML Basics modules...")
    
    tier0 = db.query(Tier).filter(Tier.tier_number == 0).first()
    if not tier0:
        print("ERROR: Tier 0 not found!")
        return
    
    # Create Python for Security module
    python_exists = db.query(Module).filter(
        Module.tier_id == tier0.id,
        Module.title == "Python for Security"
    ).first()
    
    if not python_exists:
        python_module = Module(
            tier_id=tier0.id,
            title="Python for Security",
            description="Learn Python programming for security automation, tool development, and penetration testing.",
            order=3,
            estimated_hours=6,
            is_published=True
        )
        db.add(python_module)
        db.commit()
        db.refresh(python_module)
        print("✅ Created Python for Security module")
        
        # Create 8 lesson structures
        python_lessons = [
            ("Python Basics for Security", "Python syntax, data types, control flow", 35),
            ("File Operations & Automation", "Reading/writing files, CSV, JSON", 40),
            ("Network Programming", "Sockets, HTTP requests, APIs", 45),
            ("Regular Expressions", "Pattern matching, log parsing", 35),
            ("Working with Libraries", "requests, scapy, beautifulsoup", 40),
            ("Security Tool Development", "Port scanner, password checker", 50),
            ("Web Scraping for OSINT", "Data extraction, ethical considerations", 45),
            ("Python for Automation", "Task scheduling, log analysis", 40)
        ]
        
        for i, (title, desc, duration) in enumerate(python_lessons, 1):
            lesson = Lesson(
                module_id=python_module.id,
                title=title,
                description=desc,
                order=i,
                duration_minutes=duration,
                content_markdown=f"# {title}\n\n*Comprehensive lesson content on {desc} - in development*",
                is_published=False
            )
            db.add(lesson)
        db.commit()
        print(f"  Added 8 lesson structures")
    else:
        print("Python module already exists")
    
    # Create AI & ML Basics module
    ai_exists = db.query(Module).filter(
        Module.tier_id == tier0.id,
        Module.title == "AI & ML Basics"
    ).first()
    
    if not ai_exists:
        ai_module = Module(
            tier_id=tier0.id,
            title="AI & ML Basics",
            description="Introduction to Artificial Intelligence and Machine Learning for cybersecurity applications.",
            order=4,
            estimated_hours=5,
            is_published=True
        )
        db.add(ai_module)
        db.commit()
        db.refresh(ai_module)
        print("✅ Created AI & ML Basics module")
        
        # Create 6 lesson structures
        ai_lessons = [
            ("Introduction to AI/ML", "AI vs ML vs DL, security use cases", 40),
            ("Machine Learning Fundamentals", "Supervised, unsupervised, reinforcement", 50),
            ("Data Preprocessing", "Cleaning, normalization, features", 45),
            ("Classification Algorithms", "Decision trees, SVM, random forests", 50),
            ("Neural Networks Intro", "Perceptrons, backpropagation, deep learning", 55),
            ("AI for Security Applications", "Malware detection, anomaly detection", 50)
        ]
        
        for i, (title, desc, duration) in enumerate(ai_lessons, 1):
            lesson = Lesson(
                module_id=ai_module.id,
                title=title,
                description=desc,
                order=i,
                duration_minutes=duration,
                content_markdown=f"# {title}\n\n*Comprehensive lesson content on {desc} - in development*",
                is_published=False
            )
            db.add(lesson)
        db.commit()
        print(f"  Added 6 lesson structures")
    else:
        print("AI & ML module already exists")
    
    print("\n🎉 TIER 0 COMPLETE!")
    print("  • Linux Basics (12 lessons)")
    print("  • Networking Fundamentals (10 lessons)")
    print("  • Python for Security (8 lessons)")
    print("  • AI & ML Basics (6 lessons)")
    print("  Total: 36 lessons across 4 modules")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_tier0_remaining_modules(db)
    finally:
        db.close()
