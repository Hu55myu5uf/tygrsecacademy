"""
Create progress tracking tables
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import Base, engine
from models import progress, user, curriculum

print("Creating progress tracking tables...")
print("Tables to be created:")
print("- lesson_progress")
print("- module_progress")
print("- tier_progress")

print("\nCreating tables...")
Base.metadata.create_all(bind=engine)

print("✅ Progress tracking tables created successfully!")
print("\nVerifying tables...")

from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()

if 'lesson_progress' in tables:
    print("  ✅ lesson_progress table exists")
else:
    print("  ❌ lesson_progress table missing")

if 'module_progress' in tables:
    print("  ✅ module_progress table exists")
else:
    print("  ❌ module_progress table missing")

if 'tier_progress' in tables:
    print("  ✅ tier_progress table exists")
else:
    print("  ❌ tier_progress table missing")

print("\nAll done!")
