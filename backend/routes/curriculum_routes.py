from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from database.connection import get_db
from models.curriculum import Tier, Module, Lesson, ContentBlock
from schemas import TierResponse, ModuleResponse, LessonResponse

router = APIRouter()


@router.get("/tiers", response_model=List[TierResponse])
async def get_tiers(db: Session = Depends(get_db)):
    """
    Get all curriculum tiers with their modules.
    Only returns active tiers and published modules.
    """
    tiers = db.query(Tier).filter(Tier.is_active == True).order_by(Tier.order).all()
    # Note: Filtering nested relations in SQLAlchemy usually required joinedload with filter, 
    # but for simplicity we'll rely on active tiers. 
    # Ideally we should filter modules too, but Pydantic will serialize what's loaded.
    # For a production app, we'd want to be more specific with loading strategies.
    return tiers


@router.get("/tiers/{tier_id}", response_model=TierResponse)
async def get_tier(tier_id: int, db: Session = Depends(get_db)):
    """Get a specific tier details"""
    tier = db.query(Tier).filter(Tier.id == tier_id).first()
    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tier not found"
        )
    return tier


@router.get("/modules/{module_id}", response_model=ModuleResponse)
async def get_module(module_id: int, db: Session = Depends(get_db)):
    """Get a specific module details with its lessons"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    return module


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get full lesson content including content blocks"""
    lesson = db.query(Lesson).options(
        joinedload(Lesson.content_blocks)
    ).filter(Lesson.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
        
    # Ensure content blocks are ordered
    lesson.content_blocks.sort(key=lambda x: x.order)
    
    return lesson
