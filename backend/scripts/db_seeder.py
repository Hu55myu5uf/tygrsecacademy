
import sys
import os
from sqlalchemy.orm import Session

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson, ContentBlock, ContentType

def seed_curriculum(db: Session):
    print("Seeding curriculum data...")
    
    # Check if data already exists
    if db.query(Tier).count() > 0:
        print("Curriculum data already exists. Skipping.")
        return

    # 1. Create Tiers
    tier1 = Tier(
        tier_number=1,
        name="Security Fundamentals",
        description="Build your foundation in cybersecurity concepts and terminology.",
        order=1
    )
    
    tier2 = Tier(
        tier_number=2,
        name="Network Security",
        description="Deep dive into network protocols, traffic analysis, and defense.",
        order=2
    )
    
    db.add(tier1)
    db.add(tier2)
    db.commit()
    db.refresh(tier1)
    
    # 2. Create Modules for Tier 1
    mod_intro = Module(
        tier_id=tier1.id,
        title="Introduction to Cybersecurity",
        description="Learn what cybersecurity is and why it matters.",
        order=1,
        estimated_hours=2,
        is_published=True
    )
    
    mod_principles = Module(
        tier_id=tier1.id,
        title="Core Security Principles",
        description="Understand the CIA Triad and other fundamental models.",
        order=2,
        estimated_hours=3,
        is_published=True
    )
    
    db.add(mod_intro)
    db.add(mod_principles)
    db.commit()
    db.refresh(mod_intro)
    db.refresh(mod_principles)
    
    # 3. Create Lessons for Intro Module
    lesson1 = Lesson(
        module_id=mod_intro.id,
        title="Welcome to the Academy",
        description="An overview of your learning journey.",
        order=1,
        duration_minutes=10,
        content_markdown="""
# Welcome to TygrSec Academy

We are thrilled to have you here! This platform is designed to take you from a beginner to a cybersecurity professional.

## How to use this platform
- Follow the **Curriculum** tiers in order.
- Complete **Modules** to unlock badges.
- Use the **AI Tutor** for help when you're stuck.
- Apply what you learn in our **Hands-on Labs**.
        """,
        is_published=True
    )
    
    lesson2 = Lesson(
        module_id=mod_intro.id,
        title="The Cybersecurity Landscape",
        description="Overview of current threats and career paths.",
        order=2,
        duration_minutes=15,
        content_markdown="""
# The Modern Threat Landscape

Cybersecurity is an arms race. As defenders, we must constantly evolve to meet new threats.

## Common Threat Vectors
1. **Phishing**: Social engineering attacks via email.
2. **Ransomware**: Malware that encrypts data for ransom.
3. **Insider Threats**: Risks from within the organization.
        """,
        is_published=True
    )
    
    db.add(lesson1)
    db.add(lesson2)
    db.commit()
    
    # 4. Create Lessons for Principles Module (CIA Triad)
    lesson_cia = Lesson(
        module_id=mod_principles.id,
        title="The CIA Triad",
        description="Confidentiality, Integrity, and Availability.",
        order=1,
        duration_minutes=20,
        content_markdown="""
# The CIA Triad

The core model for information security.

- **Confidentiality**: Ensuring only authorized people see the data.
- **Integrity**: Ensuring the data hasn't been tampered with.
- **Availability**: Ensuring the data is valid request accessible when needed.
        """,
        is_published=True
    )
    
    db.add(lesson_cia)
    db.commit()
    db.refresh(lesson_cia)
    
    # 5. Add a Quiz Block to CIA Lesson
    quiz_block = ContentBlock(
        lesson_id=lesson_cia.id,
        type=ContentType.QUIZ,
        order=1,
        quiz_data="""
[
    {
        "question": "Which component of the CIA triad ensures data is not altered?",
        "options": ["Confidentiality", "Integrity", "Availability"],
        "correct_index": 1
    },
    {
        "question": "Preventing unauthorized access refers to:",
        "options": ["Confidentiality", "Integrity", "Availability"],
        "correct_index": 0
    }
]
        """
    )
    
    db.add(quiz_block)
    db.commit()
    
    print("Curriculum seeded successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_curriculum(db)
    finally:
        db.close()
