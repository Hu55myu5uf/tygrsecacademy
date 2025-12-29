"""
Create Tier 3: CTF Challenges structure
Based on dashboard: OSINT, Malware Analysis, Adversarial ML, Leaderboards
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module

db = SessionLocal()

print("🚀 Creating Tier 3: CTF Challenges")
print("=" * 60)

# Create Tier 3
tier3 = db.query(Tier).filter(Tier.tier_number == 3).first()
if not tier3:
    tier3 = Tier(
        tier_number=3,
        name="CTF Challenges",
        description="Capture The Flag challenges with competitive elements and real-world scenarios",
        order=3,
        is_active=True
    )
    db.add(tier3)
    db.commit()
    print(f"✅ Created Tier 3: {tier3.name}")
else:
    print(f"✅ Tier 3 exists: {tier3.name}")

# Module 11: OSINT Challenges
m11 = db.query(Module).filter(Module.title == "OSINT Challenges").first()
if not m11:
    m11 = Module(
        tier_id=tier3.id,
        title="OSINT Challenges",
        description="Open Source Intelligence gathering and analysis challenges",
        order=11,
        estimated_hours=6,
        is_published=True
    )
    db.add(m11)
    print(f"✅ Created Module 11: {m11.title}")

# Module 12: Malware Analysis CTF
m12 = db.query(Module).filter(Module.title == "Malware Analysis CTF").first()
if not m12:
    m12 = Module(
        tier_id=tier3.id,
        title="Malware Analysis CTF",
        description="Reverse engineering and malware analysis challenges",
        order=12,
        estimated_hours=8,
        is_published=True
    )
    db.add(m12)
    print(f"✅ Created Module 12: {m12.title}")

# Module 13: Adversarial ML Challenges
m13 = db.query(Module).filter(Module.title == "Adversarial ML Challenges").first()
if not m13:
    m13 = Module(
        tier_id=tier3.id,
        title="Adversarial ML Challenges",
        description="Attack and defend machine learning models in security contexts",
        order=13,
        estimated_hours=7,
        is_published=True
    )
    db.add(m13)
    print(f"✅ Created Module 13: {m13.title}")

# Module 14: Competitive Challenges
m14 = db.query(Module).filter(Module.title == "Competitive Challenges").first()
if not m14:
    m14 = Module(
        tier_id=tier3.id,
        title="Competitive Challenges",
        description="Leaderboard-ranked challenges and team competitions",
        order=14,
        estimated_hours=5,
        is_published=True
    )
    db.add(m14)
    print(f"✅ Created Module 14: {m14.title}")

db.commit()
db.close()

print("\n✅ Tier 3 structure complete!")
print("   - Module 11: OSINT Challenges")
print("   - Module 12: Malware Analysis CTF")
print("   - Module 13: Adversarial ML Challenges")
print("   - Module 14: Competitive Challenges")
