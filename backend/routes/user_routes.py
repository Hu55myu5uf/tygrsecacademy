"""
User Routes
User management and profile endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from models.user import User, UserRole
from auth.rbac import get_current_user, require_admin, require_tutor
from schemas import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    from datetime import datetime
    
    for field, value in user_update.dict(exclude_unset=True).items():
        # Convert date_of_birth string to datetime if provided
        if field == 'date_of_birth' and value:
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                # If it's already a datetime or invalid, keep as is
                pass
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_tutor()),
    db: Session = Depends(get_db)
):
    """Get user by ID (tutor/admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """List all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


from models.progress import TierProgress, UserAchievement, Achievement  # Added imports
from schemas import UserResponse, UserUpdate, PublicProfileResponse  # Added imports

# ... (existing imports)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None


@router.get("/profile/{username}", response_model=PublicProfileResponse)
async def get_public_profile(
    username: str,
    db: Session = Depends(get_db)
):
    """Get public profile by username"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate stats
    tier_progress = db.query(TierProgress).filter(
        TierProgress.user_id == user.id,
        TierProgress.is_completed == True
    ).order_by(TierProgress.tier_id.desc()).first()
    
    current_tier = tier_progress.tier_id if tier_progress else 0
    
    # Total points (simple calculation from tier or just stored? Assuming calculation)
    # Ideally we'd have a Leaderboard entry, but let's use what we have.
    # Actually Leaderboard table has total_points.
    from models.challenge import Leaderboard
    leaderboard_entry = db.query(Leaderboard).filter(Leaderboard.user_id == user.id).first()
    total_points = leaderboard_entry.total_points if leaderboard_entry else 0
    
    # Achievements
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    achievements_data = []
    for ua in user_achievements:
        achievements_data.append({
            "name": ua.achievement.name,
            "description": ua.achievement.description,
            "icon": ua.achievement.icon_name or "Award",  # Default to Award if no icon
            "earned_at": ua.earned_at
        })
        
    return PublicProfileResponse(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        linkedin_url=user.linkedin_url,
        github_url=user.github_url,
        role=user.role,
        created_at=user.created_at,
        current_tier=current_tier,
        total_points=total_points,
        achievements=achievements_data
    )
