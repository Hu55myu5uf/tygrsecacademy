"""
Script to populate leaderboard with sample data for testing
Run this once to see the leaderboard in action
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from sqlalchemy.orm import Session
from database.connection import get_db
# Import all models to ensure proper ORM mapping
import models.user
import models.challenge
import models.curriculum
import models.lab
import models.progress
from models.user import User
from models.challenge import Leaderboard
from datetime import datetime, timedelta
import random

async def populate_leaderboard():
    db = next(get_db())
    
    try:
        # Get all users
        users = db.query(User).filter(User.role == 'student').all()
        
        if not users:
            print("No student users found. Please create some users first.")
            return
        
        print(f"Found {len(users)} student users")
        
        # Create or update leaderboard entries
        for user in users:
            # Check if entry exists
            existing = db.query(Leaderboard).filter(Leaderboard.user_id == user.id).first()
            
            if not existing:
                # Create sample data
                total_points = random.randint(100, 5000)
                challenges_solved = random.randint(1, 50)
                
                leaderboard = Leaderboard(
                    user_id=user.id,
                    total_points=total_points,
                    challenges_solved=challenges_solved,
                    easy_solved=random.randint(0, min(20, challenges_solved)),
                    medium_solved=random.randint(0, min(15, challenges_solved)),
                    hard_solved=random.randint(0, min(10, challenges_solved)),
                    insane_solved=random.randint(0, min(5, challenges_solved)),
                    last_solve_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.add(leaderboard)
                print(f"Created leaderboard entry for {user.username}: {total_points} points")
            else:
                print(f"Leaderboard entry already exists for {user.username}")
        
        db.commit()
        print("\nLeaderboard populated successfully!")
        print("Visit /student/leaderboard to see the results")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(populate_leaderboard())
