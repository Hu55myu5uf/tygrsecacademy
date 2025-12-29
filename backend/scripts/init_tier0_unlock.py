"""
Initialize Tier 0 as unlocked for existing users
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.user import User
from models.curriculum import Tier
from models.progress import TierProgress

db = SessionLocal()

print("🔓 Unlocking Tier 0 for all users...")

# Get Tier 0
tier0 = db.query(Tier).filter(Tier.tier_number == 0).first()
if not tier0:
    print("❌ Tier 0 not found! Please run tier creation scripts first.")
    db.close()
    exit(1)

# Get all users
users = db.query(User).all()

print(f"Found {len(users)} users")

for user in users:
    # Check if tier progress exists
    tier_progress = db.query(TierProgress).filter(
        TierProgress.user_id == user.id,
        TierProgress.tier_id == tier0.id
    ).first()
    
    if not tier_progress:
        # Create unlocked Tier 0 progress
        tier_progress = TierProgress(
            user_id=user.id,
            tier_id=tier0.id,
            is_unlocked=True,
            completion_percentage=0.0
        )
        db.add(tier_progress)
        print(f"  ✅ Unlocked Tier 0 for user: {user.username}")
    else:
        if not tier_progress.is_unlocked:
            tier_progress.is_unlocked = True
            print(f"  ✅ Updated Tier 0 unlock for user: {user.username}")

db.commit()
db.close()

print("\n✅ Tier 0 unlocked for all users!")
