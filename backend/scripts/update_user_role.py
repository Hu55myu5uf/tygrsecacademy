"""
Update user role
Usage: python update_user_role.py
"""
from database.connection import get_db
from models.user import User, UserRole
# Import all models to initialize relationships
import models.lab
import models.challenge
import models.curriculum
import models.progress
import models.capstone

def update_user_role(username: str, new_role: str):
    """Update a user's role"""
    db = next(get_db())
    
    try:
        # Find user
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            return
        
        # Validate role
        valid_roles = ['student', 'tutor', 'admin']
        if new_role not in valid_roles:
            print(f"❌ Invalid role! Must be one of: {valid_roles}")
            return
        
        # Update role
        old_role = user.role
        user.role = UserRole(new_role)
        db.commit()
        
        print(f"✅ Successfully updated {username}")
        print(f"   Old role: {old_role}")
        print(f"   New role: {new_role}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=== Update User Role ===\n")
    
    # Get input
    username = input("Enter username: ").strip()
    print("\nAvailable roles:")
    print("  1. student")
    print("  2. tutor")
    print("  3. admin")
    role_choice = input("\nEnter role (student/tutor/admin): ").strip().lower()
    
    update_user_role(username, role_choice)
