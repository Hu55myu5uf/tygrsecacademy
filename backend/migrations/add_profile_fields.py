"""
Add profile fields to users table
Migration to add date_of_birth, country, city, and phone_number columns
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from config import settings

DATABASE_URL = settings.DATABASE_URL

def upgrade():
    """Add new profile fields"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Add new columns
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS date_of_birth TIMESTAMP,
                ADD COLUMN IF NOT EXISTS country VARCHAR(100),
                ADD COLUMN IF NOT EXISTS city VARCHAR(100),
                ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20);
            """))
            conn.commit()
            print("✓ Successfully added profile fields to users table")
        except Exception as e:
            print(f"✗ Error adding columns: {e}")
            conn.rollback()

def downgrade():
    """Remove profile fields"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            conn.execute(text("""
                ALTER TABLE users 
                DROP COLUMN IF EXISTS date_of_birth,
                DROP COLUMN IF EXISTS country,
                DROP COLUMN IF EXISTS city,
                DROP COLUMN IF EXISTS phone_number;
            """))
            conn.commit()
            print("✓ Successfully removed profile fields from users table")
        except Exception as e:
            print(f"✗ Error removing columns: {e}")
            conn.rollback()

if __name__ == "__main__":
    print("Running migration: Add profile fields to users table")
    upgrade()
