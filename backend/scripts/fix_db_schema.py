import sys
import os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import SessionLocal

def fix():
    db = SessionLocal()
    try:
        print("🔧 Dropping achievements table...")
        db.execute(text("DROP TABLE IF EXISTS user_achievements")) # Drop dependent first
        db.execute(text("DROP TABLE IF EXISTS achievements"))
        db.commit()
        print("✅ Tables dropped.")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix()
