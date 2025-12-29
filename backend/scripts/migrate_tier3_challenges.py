import sys
import os
import re
from sqlalchemy import text, inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal, engine, Base
from models.curriculum import Lesson, Module, Tier
from models.challenge import Challenge, ChallengeCategory, ChallengeDifficulty

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def migrate():
    db = SessionLocal()
    try:
        print("🚀 Starting Tier 3 Challenge Migration")
        print("=" * 60)

        # 1. Add column if not exists
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns('lessons')]
        if 'challenge_id' not in columns:
            print("📦 Adding challenge_id column to lessons table...")
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE lessons ADD COLUMN challenge_id INTEGER REFERENCES challenges(id)"))
                conn.commit()
            print("✅ Column added.")
        else:
            print("✅ Column challenge_id already exists.")

        # 2. Get Tier 3 Modules
        modules = db.query(Module).join(Tier).filter(Tier.tier_number == 3).all()
        
        count = 0
        for module in modules:
            print(f"\nProcessing Module: {module.title}")
            
            # Determine Category
            category = ChallengeCategory.OSINT
            if "Malware" in module.title:
                category = ChallengeCategory.MALWARE_ANALYSIS
            elif "ML" in module.title:
                category = ChallengeCategory.ADVERSARIAL_ML
            elif "Competitive" in module.title:
                category = ChallengeCategory.EXPLOITATION

            lessons = db.query(Lesson).filter(Lesson.module_id == module.id).all()
            
            for lesson in lessons:
                if lesson.challenge_id:
                    print(f"  ⏭️ Lesson '{lesson.title}' already has challenge.")
                    continue

                # Create Challenge
                print(f"  ⚡ Creating challenge for '{lesson.title}'...")
                
                # Default flag for verification
                flag = "TYGR{debug_flag}"
                
                # Try to extract points
                points = 100
                pts_match = re.search(r'(\d+)\s*pts', lesson.content_markdown)
                if pts_match:
                    points = int(pts_match.group(1))

                challenge = Challenge(
                    title=f"{lesson.title} Challenge",
                    description=lesson.description,
                    category=category,
                    difficulty=ChallengeDifficulty.MEDIUM,
                    instructions=lesson.content_markdown, # Copy markdown to instructions
                    flag=flag,
                    base_points=points,
                    is_published=True
                )
                
                db.add(challenge)
                db.flush() # Get ID
                
                # Link
                lesson.challenge_id = challenge.id
                count += 1
                
        db.commit()
        print(f"\n✅ Migration Complete. Created {count} challenges.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
