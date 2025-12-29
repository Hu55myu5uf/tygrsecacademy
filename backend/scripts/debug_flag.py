import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.challenge import Challenge

def check_flag():
    db = SessionLocal()
    try:
        challenge = db.query(Challenge).filter(Challenge.id == 1).first()
        if challenge:
            print(f"Challenge 1: {challenge.title}")
            print(f"Flag in DB: '{challenge.flag}'")
            print(f"Repr: {repr(challenge.flag)}")
        else:
            print("Challenge 1 not found")
            
    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    check_flag()
