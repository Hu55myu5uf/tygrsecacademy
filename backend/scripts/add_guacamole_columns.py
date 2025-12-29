"""
Add Guacamole columns to labs table
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine
from sqlalchemy import text

def add_guacamole_columns():
    """Add lab_type, guacamole_url, and compose_file columns to labs table"""
    with engine.connect() as conn:
        try:
            # Check if columns already exist
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'labs'"))
            existing_columns = [row[0] for row in result.fetchall()]
            
            if 'lab_type' not in existing_columns:
                print("Adding lab_type column...")
                conn.execute(text("ALTER TABLE labs ADD COLUMN lab_type VARCHAR DEFAULT 'terminal'"))
            
            if 'guacamole_url' not in existing_columns:
                print("Adding guacamole_url column...")
                conn.execute(text("ALTER TABLE labs ADD COLUMN guacamole_url VARCHAR"))
            
            if 'compose_file' not in existing_columns:
                print("Adding compose_file column...")
                conn.execute(text("ALTER TABLE labs ADD COLUMN compose_file VARCHAR"))
            
            conn.commit()
            print("Columns added successfully!")
            
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()

if __name__ == "__main__":
    add_guacamole_columns()
