import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal, engine, Base
from models.progress import Achievement
import models.curriculum  # Register Lesson, Module, Tier
import models.user        # Register User
import models.challenge   # Register Challenge (needed by Lesson)
import models.lab         # Register LabInstance (needed by User)

# Ensure tables exist (including new Achievement ones)
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        print("🚀 Seeding Achievements...")
        
        achievements = [
            {
                "name": "First Step",
                "description": "Complete your first lesson",
                "icon_name": "BookOpen",
                "criteria_type": "lesson_count",
                "criteria_value": 1,
                "xp_reward": 50
            },
            {
                "name": "Module 1 Master",
                "description": "Complete Module 1: Foundations",
                "icon_name": "Award",
                "criteria_type": "module_complete",
                "criteria_value": 1, 
                "xp_reward": 100
            },
            {
                "name": "First Blood",
                "description": "Solve your first CTF challenge",
                "icon_name": "Flag",
                "criteria_type": "challenge_count",
                "criteria_value": 1,
                "xp_reward": 100
            },
            {
                "name": "Script Kiddie",
                "description": "Solve 3 CTF challenges",
                "icon_name": "Terminal",
                "criteria_type": "challenge_count",
                "criteria_value": 3,
                "xp_reward": 200
            },
            {
                "name": "Hacker",
                "description": "Solve 5 CTF challenges",
                "icon_name": "Cpu",
                "criteria_type": "challenge_count",
                "criteria_value": 5,
                "xp_reward": 500
            }
        ]
        
        count = 0
        for ach_data in achievements:
            # Check if exists
            exists = db.query(Achievement).filter(Achievement.name == ach_data["name"]).first()
            if not exists:
                ach = Achievement(**ach_data)
                db.add(ach)
                count += 1
                print(f"  ✨ Created: {ach_data['name']}")
            else:
                print(f"  ⏭️ Skipped: {ach_data['name']} (Exists)")
                
        db.commit()
        print(f"✅ Seeding Complete. Added {count} achievements.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
