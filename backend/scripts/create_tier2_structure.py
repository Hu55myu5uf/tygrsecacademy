"""
Create Tier 2: Hands-on Labs structure and seed all 27 lessons
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson

def create_tier2_structure(db):
    """Create Tier 2 and its modules"""
    print("🚀 Creating Tier 2: Hands-on Labs")
    print("=" * 60)
    
    # Create Tier 2
    tier2 = db.query(Tier).filter(Tier.tier_number == 2).first()
    if not tier2:
        tier2 = Tier(
            tier_number=2,
            name="Hands-on Labs",
            description="Practical hands-on experience with incident response, threat intelligence, and web application security",
            order=2,
            is_active=True
        )
        db.add(tier2)
        db.commit()
        print(f"✅ Created Tier 2: {tier2.name}")
    else:
        print(f"✅ Tier 2 exists: {tier2.name}")
    
    # Module 8: Incident Response Labs
    module8 = db.query(Module).filter(Module.title == "Incident Response Labs").first()
    if not module8:
        module8 = Module(
            tier_id=tier2.id,
            title="Incident Response Labs",
            description="Practical incident response scenarios and investigation techniques",
            order=8,
            estimated_hours=7,
            is_published=True
        )
        db.add(module8)
        db.commit()
        print(f"✅ Created Module 8: {module8.title}")
    
    # Module 9: Threat Intelligence Analysis
    module9 = db.query(Module).filter(Module.title == "Threat Intelligence Analysis").first()
    if not module9:
        module9 = Module(
            tier_id=tier2.id,
            title="Threat Intelligence Analysis",
            description="Advanced threat hunting and intelligence analysis techniques",
            order=9,
            estimated_hours=6,
            is_published=True
        )
        db.add(module9)
        db.commit()
        print(f"✅ Created Module 9: {module9.title}")
    
    # Module 10: Web Application Security
    module10 = db.query(Module).filter(Module.title == "Web Application Security").first()
    if not module10:
        module10 = Module(
            tier_id=tier2.id,
            title="Web Application Security",
            description="OWASP testing, exploitation, and secure web development",
            order=10,
            estimated_hours=8,
            is_published=True
        )
        db.add(module10)
        db.commit()
        print(f"✅ Created Module 10: {module10.title}")
    
    print("\n✅ Tier 2 structure complete!")
    return tier2, module8, module9, module10

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_tier2_structure(db)
    finally:
        db.close()
