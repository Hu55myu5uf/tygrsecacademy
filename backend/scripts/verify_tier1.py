"""
Verify Tier 1 completion in database
Check all modules and lessons are created and published
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson

def verify_tier1():
    db = SessionLocal()
    
    print("🔍 TIER 1 VERIFICATION")
    print("=" * 70)
    
    # Check Tier 1 exists
    tier1 = db.query(Tier).filter(Tier.tier_number == 1).first()
    if not tier1:
        print("❌ FAILED: Tier 1 not found!")
        db.close()
        return False
    
    print(f"✅ Tier 1 found: {tier1.name}")
    print(f"   Description: {tier1.description}")
    print(f"   Active: {tier1.is_active}")
    
    # Expected modules
    expected_modules = [
        ("ML for Network Security", 10),
        ("LLMs for SOC Operations", 8),
        ("AI-Powered Secure Coding", 7)
    ]
    
    total_lessons_expected = 25
    total_lessons_found = 0
    all_published = True
    
    print("\n📚 MODULE VERIFICATION")
    print("-" * 70)
    
    for idx, (module_name, expected_count) in enumerate(expected_modules, 1):
        module = db.query(Module).filter(Module.title == module_name).first()
        
        if not module:
            print(f"\n❌ Module {idx}: {module_name} - NOT FOUND")
            continue
        
        # Get lessons for this module
        lessons = db.query(Lesson).filter(Lesson.module_id == module.id).order_by(Lesson.order).all()
        lesson_count = len(lessons)
        published_count = sum(1 for l in lessons if l.is_published)
        
        status = "✅" if lesson_count == expected_count else "⚠️"
        print(f"\n{status} Module {idx}: {module_name}")
        print(f"   Module ID: {module.id}")
        print(f"   Expected Lessons: {expected_count}")
        print(f"   Found Lessons: {lesson_count}")
        print(f"   Published: {published_count}/{lesson_count}")
        
        if lesson_count != expected_count:
            print(f"   ⚠️  MISMATCH: Expected {expected_count}, found {lesson_count}")
        
        # List all lessons
        print(f"   Lessons:")
        for lesson in lessons:
            pub_status = "✅" if lesson.is_published else "❌"
            content_length = len(lesson.content_markdown) if lesson.content_markdown else 0
            print(f"      {pub_status} {lesson.order}. {lesson.title} ({content_length} chars)")
            if not lesson.is_published:
                all_published = False
        
        total_lessons_found += lesson_count
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("-" * 70)
    print(f"Expected Modules: 3")
    print(f"Expected Lessons: {total_lessons_expected}")
    print(f"Found Lessons: {total_lessons_found}")
    print(f"All Published: {'✅ YES' if all_published else '❌ NO'}")
    
    if total_lessons_found == total_lessons_expected and all_published:
        print("\n🎉 TIER 1 VERIFICATION: PASSED")
        print("All modules and lessons are complete and published!")
        success = True
    else:
        print("\n❌ TIER 1 VERIFICATION: FAILED")
        if total_lessons_found != total_lessons_expected:
            print(f"   Missing {total_lessons_expected - total_lessons_found} lessons")
        if not all_published:
            print("   Some lessons not published")
        success = False
    
    db.close()
    return success

if __name__ == "__main__":
    verify_tier1()
