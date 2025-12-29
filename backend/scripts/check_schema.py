"""
Check actual database schema for progress tables
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)

print("=" * 60)
print("LESSON_PROGRESS TABLE SCHEMA")
print("=" * 60)

if 'lesson_progress' in inspector.get_table_names():
    columns = inspector.get_columns('lesson_progress')
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
else:
    print("  ❌ Table does not exist!")

print("\n" + "=" * 60)
print("MODULE_PROGRESS TABLE SCHEMA")
print("=" * 60)

if 'module_progress' in inspector.get_table_names():
    columns = inspector.get_columns('module_progress')
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
else:
    print("  ❌ Table does not exist!")

print("\n" + "=" * 60)
print("TIER_PROGRESS TABLE SCHEMA")
print("=" * 60)

if 'tier_progress' in inspector.get_table_names():
    columns = inspector.get_columns('tier_progress')
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
else:
    print("  ❌ Table does not exist!")
