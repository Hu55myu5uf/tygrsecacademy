"""
Drop and recreate progress tables with correct schema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import Base, engine
from sqlalchemy import text
from models import progress, user, curriculum

print("Dropping existing progress tables...")
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS lesson_progress CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS module_progress CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS tier_progress CASCADE"))
    conn.commit()

print("✅ Dropped old tables")

print("\nRecreating progress tables with correct schema...")
Base.metadata.create_all(bind=engine)

print("✅ Progress tables recreated successfully!")

# Verify
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

print("\nVerifying tables:")
if 'lesson_progress' in tables:
    print("  ✅ lesson_progress")
    cols = inspector.get_columns('lesson_progress')
    print(f"     Columns: {[c['name'] for c in cols]}")
else:
    print("  ❌ lesson_progress missing")

if 'module_progress' in tables:
    print("  ✅ module_progress")  
else:
    print("  ❌ module_progress missing")

if 'tier_progress' in tables:
    print("  ✅ tier_progress")
else:
    print("  ❌ tier_progress missing")

print("\n✅ All done!")
