
import sys
import os
from sqlalchemy import text

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine

def migrate():
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        print("Migrating labs table...")
        
        try:
            # Add category column
            conn.execute(text("ALTER TABLE labs ADD COLUMN IF NOT EXISTS category VARCHAR DEFAULT 'General'"))
            print("Added category column")
        except Exception as e:
            print(f"Error adding category: {e}")

        try:
            # Add content column
            conn.execute(text("ALTER TABLE labs ADD COLUMN IF NOT EXISTS content VARCHAR"))
            print("Added content column")
        except Exception as e:
            print(f"Error adding content: {e}")
            
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
