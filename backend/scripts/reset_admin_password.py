
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
import models.labs
from models.user import User
from auth.password_handler import hash_password

def reset_password():
    db = SessionLocal()
    try:
        email = "huss@tygrsec.com"
        new_password = "tygr123"
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User {email} not found!")
            return

        hashed = hash_password(new_password)
        user.password_hash = hashed
        db.commit()
        print(f"Password for {email} reset successfully.")
        print(f"New Password: {new_password}")

    except Exception as e:
        print(f"Error resetting password: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_password()
