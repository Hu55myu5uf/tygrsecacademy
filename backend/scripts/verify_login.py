
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
import models.labs
from models.user import User
from auth.password_handler import verify_password
from config import settings

def verify():
    print(f"CWD: {os.getcwd()}")
    print(f"DB URL: {settings.DATABASE_URL}")
    
    db = SessionLocal()
    try:
        email = "huss@tygrsec.com"
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"User {email} NOT FOUND in this DB.")
            return

        print(f"User Found: ID={user.id}, Email={user.email}")
        print(f"Stored Hash: {user.password_hash[:10]}...")
        
        is_valid = verify_password("tygr123", user.password_hash)
        print(f"Password 'tygr123' Valid? {is_valid}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify()
