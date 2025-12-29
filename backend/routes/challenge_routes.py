"""
Challenge Routes
Endpoints for CTF challenges, submissions, and leaderboard
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional

from database.connection import get_db
from models.user import User
from models.challenge import Challenge, ChallengeSubmission, ChallengeDifficulty, Leaderboard
from auth.rbac import get_current_user, require_admin

# Import check_achievements (need to avoid circular import if progress_routes imports challenge_routes)
# Better to move check_achievements to a service or utils, but for now importing inside function could work, 
# or just import the router module if needed. 
# Actually, let's keep it simple. We can't easily import from routes. 
# Plan: Re-implement small check logic here or move check_achievements to a shared valid location.
# For simplicity in this session, I will replicate the check logic call or try import. 
# Given python imports, 'from routes.progress_routes import check_achievements' might fail if progress_routes imports this file.
# Let's see... progress_routes does NOT import challenge_routes. It imports models.challenge. SO IT IS SAFE.

from routes.progress_routes import check_achievements

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_challenges(
    category: str = None,
    difficulty: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all published challenges with optional filtering"""
    query = db.query(Challenge).filter(Challenge.is_published == True)
    
    if category:
        query = query.filter(Challenge.category == category)
    if difficulty:
        query = query.filter(Challenge.difficulty == difficulty)
    
    challenges = query.all()
    
    # Return with solve status for current user
    result = []
    for challenge in challenges:
        solved = db.query(ChallengeSubmission).filter(
            ChallengeSubmission.challenge_id == challenge.id,
            ChallengeSubmission.user_id == current_user.id,
            ChallengeSubmission.is_correct == True
        ).first()
        
        result.append({
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "category": challenge.category,
            "difficulty": challenge.difficulty,
            "base_points": challenge.base_points,
            "tags": challenge.tags,
            "solved": bool(solved),
            "solvers_count": db.query(ChallengeSubmission).filter(
                ChallengeSubmission.challenge_id == challenge.id,
                ChallengeSubmission.is_correct == True
            ).count()
        })
    
    return result


@router.get("/{challenge_id}", response_model=dict)
async def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific challenge details"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge or not challenge.is_published:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Check if user has solved it
    solved = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.challenge_id == challenge_id,
        ChallengeSubmission.user_id == current_user.id,
        ChallengeSubmission.is_correct == True
    ).first()
    
    return {
        "id": challenge.id,
        "title": challenge.title,
        "description": challenge.description,
        "instructions": challenge.instructions,
        "category": challenge.category,
        "difficulty": challenge.difficulty,
        "base_points": challenge.base_points,
        "files_url": challenge.files_url,
        "flag_format": challenge.flag_format,
        "tags": challenge.tags,
        "solved": bool(solved),
        "ai_assistance_enabled": challenge.ai_assistance_enabled
    }


@router.post("/{challenge_id}/submit", response_model=dict)
async def submit_flag(
    challenge_id: int,
    flag: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a flag for a challenge"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Check if already solved
    existing_solve = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.challenge_id == challenge_id,
        ChallengeSubmission.user_id == current_user.id,
        ChallengeSubmission.is_correct == True
    ).first()
    
    if existing_solve:
        return {"correct": True, "message": "Already solved", "points": 0}
    
    # Validate flag
    is_correct = (flag.strip() == challenge.flag.strip())
    
    # Calculate points (base points minus hint penalties)
    hints_used = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.challenge_id == challenge_id,
        ChallengeSubmission.user_id == current_user.id
    ).count()  # Simplified: count previous attempts as hints
    
    points = challenge.base_points
    if is_correct:
        penalty = (hints_used * challenge.hint_penalty) / 100
        points = int(points * (1 - penalty))
    else:
        points = 0
    
    # Create submission
    submission = ChallengeSubmission(
        challenge_id=challenge_id,
        user_id=current_user.id,
        submitted_flag=flag,
        is_correct=is_correct,
        points_earned=points,
        hints_used=hints_used
    )
    db.add(submission)
    
    # Update leaderboard if correct
    if is_correct:
        leaderboard = db.query(Leaderboard).filter(
            Leaderboard.user_id == current_user.id
        ).first()
        
        if not leaderboard:
            leaderboard = Leaderboard(
                user_id=current_user.id,
                total_points=0,
                challenges_solved=0,
                easy_solved=0,
                medium_solved=0,
                hard_solved=0,
                insane_solved=0
            )
            db.add(leaderboard)
        
        # Defensive check for existing nulls
        if leaderboard.total_points is None:
            leaderboard.total_points = 0
        if leaderboard.challenges_solved is None:
            leaderboard.challenges_solved = 0
        if leaderboard.easy_solved is None:
            leaderboard.easy_solved = 0
        if leaderboard.medium_solved is None:
            leaderboard.medium_solved = 0
        if leaderboard.hard_solved is None:
            leaderboard.hard_solved = 0
        if leaderboard.insane_solved is None:
            leaderboard.insane_solved = 0
            
        leaderboard.total_points += points
        leaderboard.challenges_solved += 1
        leaderboard.last_solve_at = datetime.utcnow()
        
        # Update difficulty counters
        if challenge.difficulty == ChallengeDifficulty.EASY:
            leaderboard.easy_solved += 1
        elif challenge.difficulty == ChallengeDifficulty.MEDIUM:
            leaderboard.medium_solved += 1
        elif challenge.difficulty == ChallengeDifficulty.HARD:
            leaderboard.hard_solved += 1
        elif challenge.difficulty == ChallengeDifficulty.INSANE:
            leaderboard.insane_solved += 1
    
    db.commit()
    
    # Check for achievements
    if is_correct:
        await check_achievements(current_user.id, db)
    
    return {
        "correct": is_correct,
        "message": f"Correct! You earned {points} points." if is_correct else "Incorrect flag. Try again!",
        "points_earned": points
    }


@router.get("/{challenge_id}/hints", response_model=List[dict])
async def get_hints(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available hints for a challenge"""
    hints = db.query(ChallengeHint).filter(
        ChallengeHint.challenge_id == challenge_id
    ).order_by(ChallengeHint.order).all()
    
    return [
        {
            "id": hint.id,
            "hint_level": hint.hint_level,
            "hint_text": hint.hint_text,
            "penalty_percent": hint.penalty_percent
        }
        for hint in hints
    ]


@router.get("/leaderboard/global", response_model=List[dict])
async def get_leaderboard(
    limit: int = 1000,  # Increased to show all users
    db: Session = Depends(get_db)
):
    """Get global leaderboard - now shows ALL users with points from all sources"""
    from sqlalchemy import func
    from models.progress import LessonProgress, ModuleProgress
    
    # Calculate points for each user from all sources:
    # - Challenges: from Leaderboard table
    # - Lessons: 10 points per completed lesson
    # - Modules: 50 points per completed module
    
    # Subquery for lesson points (10 points per completed lesson)
    lesson_points_subq = db.query(
        LessonProgress.user_id,
        func.count(LessonProgress.id).label('lessons_completed'),
        (func.count(LessonProgress.id) * 10).label('lesson_points')
    ).filter(
        LessonProgress.is_completed == True
    ).group_by(LessonProgress.user_id).subquery()
    
    # Subquery for module points (50 points per completed module)
    module_points_subq = db.query(
        ModuleProgress.user_id,
        func.count(ModuleProgress.id).label('modules_completed'),
        (func.count(ModuleProgress.id) * 50).label('module_points')
    ).filter(
        ModuleProgress.is_completed == True
    ).group_by(ModuleProgress.user_id).subquery()
    
    # Main query with all users
    entries = db.query(
        User,
        func.coalesce(Leaderboard.total_points, 0).label('challenge_points'),
        func.coalesce(Leaderboard.challenges_solved, 0).label('challenges_solved'),
        func.coalesce(lesson_points_subq.c.lesson_points, 0).label('lesson_points'),
        func.coalesce(lesson_points_subq.c.lessons_completed, 0).label('lessons_completed'),
        func.coalesce(module_points_subq.c.module_points, 0).label('module_points'),
        func.coalesce(module_points_subq.c.modules_completed, 0).label('modules_completed'),
        (
            func.coalesce(Leaderboard.total_points, 0) + 
            func.coalesce(lesson_points_subq.c.lesson_points, 0) + 
            func.coalesce(module_points_subq.c.module_points, 0)
        ).label('total_points'),
        Leaderboard.last_solve_at
    ).outerjoin(
        Leaderboard, User.id == Leaderboard.user_id
    ).outerjoin(
        lesson_points_subq, User.id == lesson_points_subq.c.user_id
    ).outerjoin(
        module_points_subq, User.id == module_points_subq.c.user_id
    ).order_by(
        (
            func.coalesce(Leaderboard.total_points, 0) + 
            func.coalesce(lesson_points_subq.c.lesson_points, 0) + 
            func.coalesce(module_points_subq.c.module_points, 0)
        ).desc()
    ).limit(limit).all()
    
    result = []
    for rank, (user, challenge_points, challenges_solved, lesson_points, lessons_completed, 
               module_points, modules_completed, total_points, last_solve_at) in enumerate(entries, start=1):
        result.append({
            "rank": rank,
            "username": user.username,
            "total_points": int(total_points),
            "challenge_points": int(challenge_points),
            "challenges_solved": int(challenges_solved),
            "lesson_points": int(lesson_points),
            "lessons_completed": int(lessons_completed),
            "module_points": int(module_points),
            "modules_completed": int(modules_completed),
            "last_solve_at": last_solve_at.isoformat() if last_solve_at else None
        })
    
    return result


# Admin endpoints
@router.post("/", dependencies=[Depends(require_admin)])
async def create_challenge(
    challenge_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new challenge (Admin only)"""
    challenge = Challenge(**challenge_data)
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return {"id": challenge.id, "message": "Challenge created"}
