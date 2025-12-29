"""
Migration script to change avatar_url column from VARCHAR(500) to TEXT
Run this once to update the database schema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from database.connection import get_db

def migrate_avatar_url():
    db = next(get_db())
    
    try:
        print("Migrating avatar_url column from VARCHAR(500) to TEXT...")
        
        # PostgreSQL: ALTER COLUMN type
        db.execute(text("""
            ALTER TABLE users 
            ALTER COLUMN avatar_url TYPE TEXT
        """))
        
        db.commit()
        print("✅ Migration successful! avatar_url is now TEXT type.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_avatar_url()
