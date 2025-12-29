"""
Admin Routes
API endpoints for admin dashboard functionality
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from models.user import User, UserRole
from models.progress import LessonProgress, ModuleProgress
from models.challenge import ChallengeSubmission
from models.capstone import CapstoneSubmission
from auth.rbac import get_current_user, require_admin
from schemas import UserResponse

router = APIRouter()


# ============================================
# User Management Endpoints
# ============================================

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Get all users with filtering and pagination (admin only)
    """
    query = db.query(User)
    
    # Apply filters
    if role:
        query = query.filter(User.role == UserRole(role))
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (User.username.ilike(search_pattern)) |
            (User.email.ilike(search_pattern)) |
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern))
        )
    
    users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}")
async def get_user_details(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Get detailed user information (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user stats
    lessons_completed = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.is_completed == True
    ).count()
    
    challenges_completed = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.user_id == user_id,
        ChallengeSubmission.is_correct == True
    ).count()
    
    capstone_submissions = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.user_id == user_id
    ).count()
    
    total_points = db.query(func.sum(ChallengeSubmission.points_earned)).filter(
        ChallengeSubmission.user_id == user_id,
        ChallengeSubmission.is_correct == True
    ).scalar() or 0
    
    return {
        **user.__dict__,
        "stats": {
            "lessons_completed": lessons_completed,
            "challenges_completed": challenges_completed,
            "capstone_submissions": capstone_submissions,
            "total_points": total_points
        }
    }


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role_data: dict,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Update user role (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from changing their own role
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot change your own role"
        )
    
    # Validate role
    new_role = role_data.get('role')
    if new_role not in ['student', 'tutor', 'admin']:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    old_role = user.role
    user.role = UserRole(new_role)
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Role updated successfully",
        "user_id": user.id,
        "username": user.username,
        "old_role": old_role.value,
        "new_role": user.role.value
    }


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status_data: dict,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Suspend or activate user (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from suspending themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot change your own status"
        )
    
    is_active = status_data.get('is_active')
    if is_active is None:
        raise HTTPException(status_code=400, detail="is_active field required")
    
    user.is_active = is_active
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": f"User {'activated' if is_active else 'suspended'} successfully",
        "user_id": user.id,
        "username": user.username,
        "is_active": user.is_active
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Soft delete user (set is_active = false) (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )
    
    # Soft delete
    user.is_active = False
    
    db.commit()
    
    return {
        "message": "User deleted successfully",
        "user_id": user.id,
        "username": user.username
    }


# ============================================
# Platform Statistics
# ============================================

@router.get("/stats")
async def get_platform_stats(
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Get platform statistics overview (admin only)
    """
    # User stats
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    students = db.query(User).filter(User.role == UserRole.STUDENT).count()
    tutors = db.query(User).filter(User.role == UserRole.TUTOR).count()
    admins = db.query(User).filter(User.role == UserRole.ADMIN).count()
    
    # Content completion stats
    total_lessons_completed = db.query(LessonProgress).filter(
        LessonProgress.is_completed == True
    ).count()
    total_challenges_completed = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.is_correct == True
    ).count()
    
    # Capstone stats
    total_capstone_submissions = db.query(CapstoneSubmission).count()
    pending_submissions = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.status == 'submitted'
    ).count()
    
    # Recent users (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_30d = db.query(User).filter(
        User.created_at >= thirty_days_ago
    ).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "students": students,
            "tutors": tutors,
            "admins": admins,
            "new_30d": new_users_30d
        },
        "engagement": {
            "lessons_completed": total_lessons_completed,
            "challenges_completed": total_challenges_completed,
            "capstone_submissions": total_capstone_submissions
        },
        "capstones": {
            "total_submissions": total_capstone_submissions,
            "pending_review": pending_submissions
        }
    }
