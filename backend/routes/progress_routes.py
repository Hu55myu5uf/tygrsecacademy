"""
Progress Tracking API Routes
Handle lesson, module, and tier progress tracking
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from models.user import User
from models.progress import LessonProgress, ModuleProgress, TierProgress, Achievement, UserAchievement
from models.curriculum import Tier, Module, Lesson
from auth.rbac import get_current_user

router = APIRouter(tags=["progress"])


# Test user helper removed - using real auth now


@router.get("/me")
async def get_my_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's detailed progress for dashboard"""
    # Sync achievements first (retroactive check)
    await check_achievements(current_user.id, db)

    # 1. Calculate Overall Stats
    total_lessons_completed = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.is_completed == True
    ).count()

    total_modules_completed = db.query(ModuleProgress).filter(
        ModuleProgress.user_id == current_user.id,
        ModuleProgress.is_completed == True
    ).count()

    # Calculate total time
    total_time_minutes = db.query(func.sum(LessonProgress.time_spent_minutes)).filter(
        LessonProgress.user_id == current_user.id
    ).scalar() or 0

    # Get current tier
    current_tier_progress = db.query(TierProgress).filter(
        TierProgress.user_id == current_user.id,
        TierProgress.is_unlocked == True
    ).order_by(TierProgress.tier_id.desc()).first()
    
    current_tier_number = 0
    if current_tier_progress:
        tier = db.query(Tier).filter(Tier.id == current_tier_progress.tier_id).first()
        if tier:
            current_tier_number = tier.tier_number

    # Mock achievements (feature not implemented yet)
    # Mock achievements (feature not implemented yet)
    # in future: db.query(UserAchievement).filter(...)
    user_achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id
    ).all()
    
    achievements_data = []
    for ua in user_achievements:
        achievements_data.append({
            "name": ua.achievement.name,
            "description": ua.achievement.description,
            "icon_url": ua.achievement.icon_name, # Mapping name to frontend icon logic
            "earned_at": ua.earned_at
        })

    # 2. Build Module List
    modules_data = []
    all_modules = db.query(Module).all()
    
    for module in all_modules:
        # Get module progress
        mp = db.query(ModuleProgress).filter(
            ModuleProgress.user_id == current_user.id,
            ModuleProgress.module_id == module.id
        ).first()

        # Get lessons stats for this module
        module_lessons = db.query(Lesson).filter(Lesson.module_id == module.id).all()
        lesson_ids = [l.id for l in module_lessons]
        
        lessons_completed_count = db.query(LessonProgress).filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.lesson_id.in_(lesson_ids),
            LessonProgress.is_completed == True
        ).count()

        module_time = db.query(func.sum(LessonProgress.time_spent_minutes)).filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.lesson_id.in_(lesson_ids)
        ).scalar() or 0

        modules_data.append({
            "module_id": module.id,
            "title": module.title,
            "completion_percent": mp.completion_percentage if mp else 0.0,
            "is_completed": mp.is_completed if mp else False,
            "lessons_completed": lessons_completed_count,
            "total_lessons": len(module_lessons),
            "time_spent_minutes": module_time
        })

    # Sort modules by id? or order? Assuming ID assumes order for now
    modules_data.sort(key=lambda x: x["module_id"])

    return {
        "overall": {
            "current_tier": current_tier_number,
            "modules_completed": total_modules_completed,
            "labs_completed": 0, # Lab tracking not yet implemented
            "challenges_solved": 0, # Challenge tracking to be fixed separately or derived
            "total_points": total_lessons_completed * 10, # Mock points
            "total_achievements": len(achievements_data),
            "total_time_minutes": total_time_minutes
        },
        "modules": modules_data,
        "achievements": achievements_data
    }


async def check_achievements(user_id: int, db: Session):
    """Internal function to check and award achievements"""
    # Get all possible achievements
    all_achievements = db.query(Achievement).all()
    
    # Get user stats
    lesson_count = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id, LessonProgress.is_completed == True
    ).count()
    
    # Need to check challenges too (circular import risk if importing Challenge routes/models here? No, models are fine)
    # We will import ChallengeSubmission inside function or at top if safe
    from models.challenge import ChallengeSubmission
    challenge_count = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.user_id == user_id, ChallengeSubmission.is_correct == True
    ).count()

    module_completions = db.query(ModuleProgress).filter(
        ModuleProgress.user_id == user_id, ModuleProgress.is_completed == True
    ).all()
    completed_module_ids = [m.module_id for m in module_completions]
    
    newly_awarded = False
    
    for ach in all_achievements:
        # Check if already earned
        earned = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == ach.id
        ).first()
        
        if earned:
            continue
            
        award = False
        
        if ach.criteria_type == 'lesson_count':
            if lesson_count >= ach.criteria_value:
                award = True
        elif ach.criteria_type == 'challenge_count':
            if challenge_count >= ach.criteria_value:
                award = True
        elif ach.criteria_type == 'module_complete':
            if ach.criteria_value in completed_module_ids:
                award = True
                
        if award:
            new_ach = UserAchievement(user_id=user_id, achievement_id=ach.id)
            db.add(new_ach)
            newly_awarded = True
            
    if newly_awarded:
        db.commit()


# ===== LESSON PROGRESS =====

@router.post("/lessons/{lesson_id}/start")
async def start_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Using test user
):
    """Mark a lesson as started"""
    # Check if lesson exists
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Check if progress already exists
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return {
        "lesson_id": lesson_id,
        "started": True,
        "started_at": progress.started_at
    }


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    time_spent: Optional[int] = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a lesson as completed"""
    # Get or create lesson progress
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.add(progress)
    
    # Update completion
    progress.is_completed = True
    progress.completed_at = datetime.now()
    progress.time_spent_minutes = time_spent
    
    db.commit()
    db.refresh(progress)
    
    # Update module progress
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson:
        await update_module_progress(current_user.id, lesson.module_id, db)
        
    # Check for achievements
    await check_achievements(current_user.id, db)
    
    return {
        "lesson_id": lesson_id,
        "is_completed": True,
        "completed_at": progress.completed_at
    }


@router.get("/lessons/{lesson_id}")
async def get_lesson_progress(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress for a specific lesson"""
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        return {
            "lesson_id": lesson_id,
            "is_completed": False,
            "started_at": None,
            "completed_at": None
        }
    
    return {
        "lesson_id": lesson_id,
        "is_completed": progress.is_completed,
        "started_at": progress.started_at,
        "completed_at": progress.completed_at,
        "time_spent_minutes": progress.time_spent_minutes
    }


# ===== MODULE PROGRESS =====

async def update_module_progress(user_id: int, module_id: int, db: Session):
    """Internal function to update module progress based on lessons"""
    # Get module with lessons
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        return
    
    # Count completed lessons
    total_lessons = len(module.lessons)
    if total_lessons == 0:
        return
    
    completed_lessons = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_id.in_([l.id for l in module.lessons]),
        LessonProgress.is_completed == True
    ).count()
    
    # Calculate percentage
    percentage = (completed_lessons / total_lessons) * 100
    
    # Get or create module progress
    module_progress = db.query(ModuleProgress).filter(
        ModuleProgress.user_id == user_id,
        ModuleProgress.module_id == module_id
    ).first()
    
    if not module_progress:
        module_progress = ModuleProgress(
            user_id=user_id,
            module_id=module_id
        )
        db.add(module_progress)
    
    # Update progress
    module_progress.completion_percentage = percentage
    module_progress.is_completed = (percentage == 100.0)
    
    if module_progress.is_completed and not module_progress.completed_at:
        module_progress.completed_at = datetime.now()
    
    db.commit()
    
    # Update tier progress
    tier = db.query(Tier).join(Module).filter(Module.id == module_id).first()
    if tier:
        await update_tier_progress(user_id, tier.id, db)


@router.get("/modules/{module_id}")
async def get_module_progress(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress for a specific module"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Get module progress
    module_progress = db.query(ModuleProgress).filter(
        ModuleProgress.user_id == current_user.id,
        ModuleProgress.module_id == module_id
    ).first()
    
    # Get lesson progress
    lesson_ids = [l.id for l in module.lessons]
    lesson_progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id.in_(lesson_ids)
    ).all()
    
    completed_count = sum(1 for lp in lesson_progress if lp.is_completed)
    
    # Create lesson progress map
    lesson_status = []
    for lesson in module.lessons:
        lp = next((p for p in lesson_progress if p.lesson_id == lesson.id), None)
        lesson_status.append({
            "lesson_id": lesson.id,
            "title": lesson.title,
            "is_completed": lp.is_completed if lp else False,
            "time_spent_minutes": lp.time_spent_minutes if lp else 0
        })

    return {
        "module_id": module_id,
        "completion_percentage": module_progress.completion_percentage if module_progress else 0.0,
        "is_completed": module_progress.is_completed if module_progress else False,
        "lessons_completed": completed_count,
        "total_lessons": len(module.lessons),
        "started_at": module_progress.started_at if module_progress else None,
        "completed_at": module_progress.completed_at if module_progress else None,
        "lessons": lesson_status
    }


@router.get("/modules")
async def get_all_module_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress for all modules"""
    results = db.query(ModuleProgress, Module).join(
        Module, ModuleProgress.module_id == Module.id
    ).filter(
        ModuleProgress.user_id == current_user.id
    ).all()
    
    return [
        {
            "module_id": p.module_id,
            "module_title": m.title,
            "tier_id": m.tier_id,
            "completion_percentage": p.completion_percentage,
            "is_completed": p.is_completed,
            "started_at": p.started_at,
            "completed_at": p.completed_at
        }
        for p, m in results
    ]


# ===== TIER PROGRESS =====

async def update_tier_progress(user_id: int, tier_id: int, db: Session):
    """Internal function to update tier progress based on modules"""
    # Get tier with modules
    tier = db.query(Tier).filter(Tier.id == tier_id).first()
    if not tier:
        return
    
    # Count completed modules
    total_modules = len(tier.modules)
    if total_modules == 0:
        return
    
    completed_modules = db.query(ModuleProgress).filter(
        ModuleProgress.user_id == user_id,
        ModuleProgress.module_id.in_([m.id for m in tier.modules]),
        ModuleProgress.is_completed == True
    ).count()
    
    # Calculate percentage
    percentage = (completed_modules / total_modules) * 100
    
    # Get or create tier progress
    tier_progress = db.query(TierProgress).filter(
        TierProgress.user_id == user_id,
        TierProgress.tier_id == tier_id
    ).first()
    
    if not tier_progress:
        tier_progress = TierProgress(
            user_id=user_id,
            tier_id=tier_id,
            is_unlocked=(tier.tier_number == 0)  # Tier 0 always unlocked
        )
        db.add(tier_progress)
    
    # Update progress
    tier_progress.completion_percentage = percentage
    tier_progress.is_completed = (percentage == 100.0)
    
    if tier_progress.is_completed and not tier_progress.completed_at:
        tier_progress.completed_at = datetime.now()
        
        # Unlock next tier
        next_tier = db.query(Tier).filter(Tier.tier_number == tier.tier_number + 1).first()
        if next_tier:
            next_tier_progress = db.query(TierProgress).filter(
                TierProgress.user_id == user_id,
                TierProgress.tier_id == next_tier.id
            ).first()
            
            if not next_tier_progress:
                next_tier_progress = TierProgress(
                    user_id=user_id,
                    tier_id=next_tier.id,
                    is_unlocked=True
                )
                db.add(next_tier_progress)
            else:
                next_tier_progress.is_unlocked = True
    
    db.commit()


@router.get("/tiers/{tier_number}")
async def get_tier_progress(
    tier_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress for a specific tier"""
    tier = db.query(Tier).filter(Tier.tier_number == tier_number).first()
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    tier_progress = db.query(TierProgress).filter(
        TierProgress.user_id == current_user.id,
        TierProgress.tier_id == tier.id
    ).first()
    
    # If no progress exists, tier 0 is unlocked by default
    if not tier_progress:
        is_unlocked = (tier_number == 0)
        return {
            "tier_number": tier_number,
            "is_unlocked": is_unlocked,
            "is_completed": False,
            "completion_percentage": 0.0
        }
    
    return {
        "tier_number": tier_number,
        "is_unlocked": tier_progress.is_unlocked,
        "is_completed": tier_progress.is_completed,
        "completion_percentage": tier_progress.completion_percentage,
        "started_at": tier_progress.started_at,
        "completed_at": tier_progress.completed_at
    }


@router.get("/tiers")
async def get_all_tier_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress for all tiers"""
    # Get all tiers
    tiers = db.query(Tier).order_by(Tier.tier_number).all()
    
    result = []
    for tier in tiers:
        tier_progress = db.query(TierProgress).filter(
            TierProgress.user_id == current_user.id,
            TierProgress.tier_id == tier.id
        ).first()
        
        if tier_progress:
            result.append({
                "tier_number": tier.tier_number,
                "tier_name": tier.name,
                "is_unlocked": tier_progress.is_unlocked,
                "is_completed": tier_progress.is_completed,
                "completion_percentage": tier_progress.completion_percentage
            })
        else:
            # Tier 0 is always unlocked
            result.append({
                "tier_number": tier.tier_number,
                "tier_name": tier.name,
                "is_unlocked": (tier.tier_number == 0),
                "is_completed": False,
                "completion_percentage": 0.0
            })
    
    return result


# ===== DASHBOARD STATS =====

@router.get("/stats")
async def get_progress_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall progress statistics for dashboard"""
    # Count completed lessons
    total_lessons_completed = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.is_completed == True
    ).count()
    
    # Count completed modules
    total_modules_completed = db.query(ModuleProgress).filter(
        ModuleProgress.user_id == current_user.id,
        ModuleProgress.is_completed == True
    ).count()
    
    # Get current tier (highest unlocked)
    current_tier_progress = db.query(TierProgress).filter(
        TierProgress.user_id == current_user.id,
        TierProgress.is_unlocked == True
    ).order_by(TierProgress.tier_id.desc()).first()
    
    current_tier = 0
    if current_tier_progress:
        tier = db.query(Tier).filter(Tier.id == current_tier_progress.tier_id).first()
        if tier:
            current_tier = tier.tier_number
    
    # Calculate total time spent
    total_time_minutes = db.query(func.sum(LessonProgress.time_spent_minutes)).filter(
        LessonProgress.user_id == current_user.id
    ).scalar() or 0
    
    # Get total lessons available
    total_lessons = db.query(Lesson).filter(Lesson.is_published == True).count()
    completion_percentage = (total_lessons_completed / total_lessons * 100) if total_lessons > 0 else 0
    
    return {
        "total_lessons_completed": total_lessons_completed,
        "total_lessons": total_lessons,
        "total_modules_completed": total_modules_completed,
        "current_tier": current_tier,
        "total_time_minutes": total_time_minutes,
        "completion_percentage": round(completion_percentage, 1)
    }
