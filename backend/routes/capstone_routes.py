"""
Capstone Project Routes
API endpoints for capstone project management, submission, and grading
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from database.connection import get_db
from models.capstone import CapstoneTier, CapstoneSubmission, SubmissionStatus
from models.user import User
from auth.rbac import get_current_user, require_tutor, require_admin
from schemas import (
    CapstoneTierResponse, CapstoneTierCreate, CapstoneTierUpdate,
    CapstoneSubmissionResponse, CapstoneSubmissionCreate, CapstoneSubmissionUpdate,
    CapstoneGradeRequest, CapstoneFeatureRequest
)

router = APIRouter()


# ============================================
# Student Endpoints
# ============================================

@router.get("/tiers", response_model=List[CapstoneTierResponse])
async def get_capstone_tiers(db: Session = Depends(get_db)):
    """List all active capstone tiers with requirements"""
    tiers = db.query(CapstoneTier).filter(CapstoneTier.is_active == True).all()
    return tiers


@router.get("/tier/{tier_id}", response_model=CapstoneTierResponse)
async def get_capstone_tier(
    tier_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed capstone requirements for a specific tier"""
    capstone_tier = db.query(CapstoneTier).filter(
        CapstoneTier.tier_id == tier_id,
        CapstoneTier.is_active == True
    ).first()
    
    if not capstone_tier:
        raise HTTPException(status_code=404, detail="Capstone tier not found")
    
    return capstone_tier


@router.get("/my-submissions", response_model=List[CapstoneSubmissionResponse])
async def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List current user's capstone submissions across all tiers"""
    submissions = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.user_id == current_user.id
    ).order_by(desc(CapstoneSubmission.created_at)).all()
    
    # Enrich with related data
    result = []
    for sub in submissions:
        sub_dict = {
            **sub.__dict__,
            "capstone_tier_title": sub.capstone_tier.title if sub.capstone_tier else None,
            "user_username": current_user.username,
            "grader_username": sub.grader.username if sub.grader else None
        }
        result.append(CapstoneSubmissionResponse(**sub_dict))
    
    return result


@router.get("/submission/{submission_id}", response_model=CapstoneSubmissionResponse)
async def get_submission(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific submission (own submission only)"""
    submission = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.id == submission_id,
        CapstoneSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": submission.capstone_tier.title if submission.capstone_tier else None,
        "user_username": current_user.username,
        "grader_username": submission.grader.username if submission.grader else None
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


@router.post("/tier/{capstone_tier_id}/submit", response_model=CapstoneSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    capstone_tier_id: int,
    submission_data: CapstoneSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new capstone submission (draft)"""
    # Verify capstone tier exists
    capstone_tier = db.query(CapstoneTier).filter(CapstoneTier.id == capstone_tier_id).first()
    if not capstone_tier:
        raise HTTPException(status_code=404, detail="Capstone tier not found")
    
    # Check if user already has a submission for this tier
    existing = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.user_id == current_user.id,
        CapstoneSubmission.capstone_tier_id == capstone_tier_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="You already have a submission for this tier. Use update endpoint instead."
        )
    
    # Create submission
    submission = CapstoneSubmission(
        user_id=current_user.id,
        capstone_tier_id=capstone_tier_id,
        **submission_data.dict()
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": capstone_tier.title,
        "user_username": current_user.username,
        "grader_username": None
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


@router.put("/submission/{submission_id}", response_model=CapstoneSubmissionResponse)
async def update_submission(
    submission_id: int,
    submission_data: CapstoneSubmissionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update submission (only if status is 'draft' or 'rejected')"""
    submission = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.id == submission_id,
        CapstoneSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Only allow edits for draft or rejected submissions
    if submission.status not in [SubmissionStatus.DRAFT, SubmissionStatus.REJECTED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot edit submission with status '{submission.status}'"
        )
    
    # Update fields
    for field, value in submission_data.dict(exclude_unset=True).items():
        setattr(submission, field, value)
    
    db.commit()
    db.refresh(submission)
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": submission.capstone_tier.title if submission.capstone_tier else None,
        "user_username": current_user.username,
        "grader_username": submission.grader.username if submission.grader else None
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


@router.post("/submission/{submission_id}/submit", response_model=CapstoneSubmissionResponse)
async def submit_final(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark submission as 'submitted' (final submission)"""
    submission = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.id == submission_id,
        CapstoneSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    if submission.status != SubmissionStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot submit submission with status '{submission.status}'"
        )
    
    # Update status
    submission.status = SubmissionStatus.SUBMITTED
    submission.submitted_at = datetime.utcnow()
    
    db.commit()
    db.refresh(submission)
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": submission.capstone_tier.title if submission.capstone_tier else None,
        "user_username": current_user.username,
        "grader_username": None
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


# ============================================
# Instructor/Admin Endpoints
# ============================================

@router.get("/admin/submissions", response_model=List[CapstoneSubmissionResponse])
async def get_all_submissions(
    tier_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_tutor()),
    db: Session = Depends(get_db)
):
    """List all submissions with filters (instructor/admin only)"""
    query = db.query(CapstoneSubmission)
    
    # Apply filters
    if tier_id:
        query = query.join(CapstoneTier).filter(CapstoneTier.tier_id == tier_id)
    
    if status_filter:
        query = query.filter(CapstoneSubmission.status == status_filter)
    
    if user_id:
        query = query.filter(CapstoneSubmission.user_id == user_id)
    
    submissions = query.order_by(desc(CapstoneSubmission.submitted_at)).offset(skip).limit(limit).all()
    
    # Enrich with related data
    result = []
    for sub in submissions:
        sub_dict = {
            **sub.__dict__,
            "capstone_tier_title": sub.capstone_tier.title if sub.capstone_tier else None,
            "user_username": sub.user.username if sub.user else None,
            "grader_username": sub.grader.username if sub.grader else None
        }
        result.append(CapstoneSubmissionResponse(**sub_dict))
    
    return result


@router.get("/admin/submission/{submission_id}", response_model=CapstoneSubmissionResponse)
async def get_submission_for_grading(
    submission_id: int,
    current_user: User = Depends(require_tutor()),
    db: Session = Depends(get_db)
):
    """Get any submission for grading (instructor/admin only)"""
    submission = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": submission.capstone_tier.title if submission.capstone_tier else None,
        "user_username": submission.user.username if submission.user else None,
        "grader_username": submission.grader.username if submission.grader else None
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


@router.put("/admin/submission/{submission_id}/grade", response_model=CapstoneSubmissionResponse)
async def grade_submission(
    submission_id: int,
    grade_data: CapstoneGradeRequest,
    current_user: User = Depends(require_tutor()),
    db: Session = Depends(get_db)
):
    """Grade a submission (instructor/admin only)"""
    submission = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Update grading fields
    submission.score = grade_data.score
    submission.feedback = grade_data.feedback
    submission.rubric_evaluation = grade_data.rubric_evaluation
    submission.status = SubmissionStatus(grade_data.status)
    submission.graded_by = current_user.id
    submission.graded_at = datetime.utcnow()
    
    db.commit()
    db.refresh(submission)
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": submission.capstone_tier.title if submission.capstone_tier else None,
        "user_username": submission.user.username if submission.user else None,
        "grader_username": current_user.username
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


@router.put("/admin/submission/{submission_id}/feature", response_model=CapstoneSubmissionResponse)
async def toggle_feature(
    submission_id: int,
    feature_data: CapstoneFeatureRequest,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Toggle submission featured status for showcase (admin only)"""
    submission = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    submission.is_featured = feature_data.is_featured
    
    db.commit()
    db.refresh(submission)
    
    # Enrich with related data
    sub_dict = {
        **submission.__dict__,
        "capstone_tier_title": submission.capstone_tier.title if submission.capstone_tier else None,
        "user_username": submission.user.username if submission.user else None,
        "grader_username": submission.grader.username if submission.grader else None
    }
    
    return CapstoneSubmissionResponse(**sub_dict)


# ============================================
# Admin - Tier Management
# ============================================

@router.post("/admin/tier", response_model=CapstoneTierResponse, status_code=status.HTTP_201_CREATED)
async def create_capstone_tier(
    tier_data: CapstoneTierCreate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Create new capstone tier definition (admin only)"""
    # Check if tier already has a capstone
    existing = db.query(CapstoneTier).filter(CapstoneTier.tier_id == tier_data.tier_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="This tier already has a capstone project defined"
        )
    
    capstone_tier = CapstoneTier(**tier_data.dict())
    
    db.add(capstone_tier)
    db.commit()
    db.refresh(capstone_tier)
    
    return capstone_tier


@router.put("/admin/tier/{capstone_tier_id}", response_model=CapstoneTierResponse)
async def update_capstone_tier(
    capstone_tier_id: int,
    tier_data: CapstoneTierUpdate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """Update capstone tier requirements (admin only)"""
    capstone_tier = db.query(CapstoneTier).filter(CapstoneTier.id == capstone_tier_id).first()
    
    if not capstone_tier:
        raise HTTPException(status_code=404, detail="Capstone tier not found")
    
    # Update fields
    for field, value in tier_data.dict(exclude_unset=True).items():
        setattr(capstone_tier, field, value)
    
    db.commit()
    db.refresh(capstone_tier)
    
    return capstone_tier


# ============================================
# Public Endpoints
# ============================================

@router.get("/showcase", response_model=List[CapstoneSubmissionResponse])
async def get_showcase(
    tier_id: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List featured capstone submissions for gallery (public)"""
    query = db.query(CapstoneSubmission).filter(
        CapstoneSubmission.is_featured == True,
        CapstoneSubmission.status == SubmissionStatus.APPROVED
    )
    
    if tier_id:
        query = query.join(CapstoneTier).filter(CapstoneTier.tier_id == tier_id)
    
    submissions = query.order_by(desc(CapstoneSubmission.graded_at)).limit(limit).all()
    
    # Enrich with related data (hide sensitive info for public)
    result = []
    for sub in submissions:
        sub_dict = {
            **sub.__dict__,
            "capstone_tier_title": sub.capstone_tier.title if sub.capstone_tier else None,
            "user_username": sub.user.username if sub.user else None,
            "grader_username": None,  # Hide grader for public
            "feedback": None  # Hide feedback for public
        }
        result.append(CapstoneSubmissionResponse(**sub_dict))
    
    return result
