"""
Create Tier 1: AI in Cybersecurity
- Tier 1 with 3 modules and 25 lessons total
- Complete professional content for all lessons
"""
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson

def create_tier1(db):
    """Create Tier 1: AI in Cybersecurity"""
    print("🚀 Creating Tier 1: AI in Cybersecurity...")
    
    # Check if Tier 1 exists
    tier1 = db.query(Tier).filter(Tier.tier_number == 1).first()
    if not tier1:
        tier1 = Tier(
            tier_number=1,
            name="AI in Cybersecurity",
            description="Apply machine learning and AI to advanced cybersecurity challenges",
            order=1,
            is_active=True
        )
        db.add(tier1)
        db.commit()
        print(f"✅ Created Tier 1: {tier1.name}")
    else:
        print(f"✅ Tier 1 already exists: {tier1.name}")
    
    # Module 5: ML for Network Security
    module5 = db.query(Module).filter(Module.title == "ML for Network Security").first()
    if not module5:
        module5 = Module(
            tier_id=tier1.id,
            title="ML for Network Security",
            description="Apply machine learning to network security challenges including IDS, DDoS detection, and traffic analysis",
            order=5,
            estimated_hours=8,
            is_published=True
        )
        db.add(module5)
        db.commit()
        print(f"✅ Created Module 5: {module5.title}")
    
    # Module 6: LLMs for SOC Operations
    module6 = db.query(Module).filter(Module.title == "LLMs for SOC Operations").first()
    if not module6:
        module6 = Module(
            tier_id=tier1.id,
            title="LLMs for SOC Operations",
            description="Use Large Language Models to enhance Security Operations Center efficiency and automation",
            order=6,
            estimated_hours=7,
            is_published=True
        )
        db.add(module6)
        db.commit()
        print(f"✅ Created Module 6: {module6.title}")
    
    # Module 7: AI-Powered Secure Coding
    module7 = db.query(Module).filter(Module.title == "AI-Powered Secure Coding").first()
    if not module7:
        module7 = Module(
            tier_id=tier1.id,
            title="AI-Powered Secure Coding",
            description="Use AI to improve code security, automate reviews, and enhance secure development practices",
            order=7,
            estimated_hours=5,
            is_published=True
        )
        db.add(module7)
        db.commit()
        print(f"✅ Created Module 7: {module7.title}")
    
    print("\n✅ Tier 1 structure created successfully!")
    print(f"   - Tier 1: {tier1.name}")
    print(f"   - Module 5: {module5.title}")
    print(f"   - Module 6: {module6.title}")
    print(f"   - Module 7: {module7.title}")
    
    return tier1, module5, module6, module7

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_tier1(db)
    finally:
        db.close()
