"""
Create Tier 4: Mastery & Publishing structure
Based on dashboard: Capstone Projects, Tutor Supervision, Blog Publishing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module

db = SessionLocal()

print("🚀 Creating Tier 4: Mastery & Publishing")
print("=" * 60)

# Create Tier 4
tier4 = db.query(Tier).filter(Tier.tier_number == 4).first()
if not tier4:
    tier4 = Tier(
        tier_number=4,
        name="Mastery & Publishing",
        description="Capstone projects, professional mentorship, and knowledge sharing through blogging",
        order=4,
        is_active=True
    )
    db.add(tier4)
    db.commit()
    print(f"✅ Created Tier 4: {tier4.name}")
else:
    print(f"✅ Tier 4 exists: {tier4.name}")

# Module 15: Capstone Projects
m15 = db.query(Module).filter(Module.title == "Capstone Projects").first()
if not m15:
    m15 = Module(
        tier_id=tier4.id,
        title="Capstone Projects",
        description="Comprehensive real-world security projects demonstrating mastery",
        order=15,
        estimated_hours=10,
        is_published=True
    )
    db.add(m15)
    print(f"✅ Created Module 15: {m15.title}")

# Module 16: Tutor Supervision
m16 = db.query(Module).filter(Module.title == "Tutor Supervision").first()
if not m16:
    m16 = Module(
        tier_id=tier4.id,
        title="Tutor Supervision",
        description="One-on-one mentorship and professional guidance",
        order=16,
        estimated_hours=8,
        is_published=True
    )
    db.add(m16)
    print(f"✅ Created Module 16: {m16.title}")

# Module 17: Security Blogging
m17 = db.query(Module).filter(Module.title == "Security Blogging").first()
if not m17:
    m17 = Module(
        tier_id=tier4.id,
        title="Security Blogging",
        description="Build your professional brand through technical writing and publishing",
        order=17,
        estimated_hours=6,
        is_published=True
    )
    db.add(m17)
    print(f"✅ Created Module 17: {m17.title}")

db.commit()
db.close()

print("\n✅ Tier 4 structure complete!")
print("   - Module 15: Capstone Projects")
print("   - Module 16: Tutor Supervision")
print("   - Module 17: Security Blogging")
