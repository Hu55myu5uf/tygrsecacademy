"""
AI Tutor Routes
API endpoints for AI-powered tutoring, hints, and recommendations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import logging

from database.connection import get_db
from auth.rbac import get_current_user
from models.user import User
from models.ai_context import AIConversation
from models.curriculum import Lesson, Module
from models.challenge import Challenge
from models.labs import Lab
from services.ai_service import ai_service

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    context_type: str  # lesson, lab, challenge
    context_id: int


class ChatResponse(BaseModel):
    response: str
    tokens_used: int
    response_time_ms: int


class HintRequest(BaseModel):
    context_type: str  # lab, challenge
    context_id: int
    hint_level: int = 1  # 1=gentle, 2=specific, 3=direct


class HintResponse(BaseModel):
    hint: str
    level: int


class ConversationHistoryItem(BaseModel):
    id: int
    user_message: str
    ai_response: str
    created_at: str


# Helper function to get context data
def get_context_data(context_type: str, context_id: int, db: Session) -> dict:
    """Fetch context data based on type and ID"""
    if context_type == "lesson":
        lesson = db.query(Lesson).filter(Lesson.id == context_id).first()
        if lesson:
            return {
                "title": lesson.title,
                "description": lesson.description,
                "content": lesson.content_markdown[:2000] if lesson.content_markdown else ""  # Limit for token efficiency
            }
    elif context_type == "lab":
        lab = db.query(Lab).filter(Lab.id == context_id).first()
        if lab:
            return {
                "title": lab.title,
                "description": lab.description,
                "objectives": lab.objectives if hasattr(lab, 'objectives') else []
            }
    elif context_type == "challenge":
        challenge = db.query(Challenge).filter(Challenge.id == context_id).first()
        if challenge:
            return {
                "title": challenge.title,
                "description": challenge.description,
                "category": challenge.category,
                "difficulty": challenge.difficulty
            }
    
    return {"title": "Unknown", "description": "Context not found"}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI tutor with context awareness.
    The AI will provide guidance based on the current lesson, lab, or challenge.
    """
    try:
        # Validate context type
        if request.context_type not in ["lesson", "lab", "challenge"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid context type. Must be 'lesson', 'lab', or 'challenge'"
            )
        
        # Get context data
        context_data = get_context_data(request.context_type, request.context_id, db)
        
        # Get recent conversation history for this context
        history = db.query(AIConversation).filter(
            AIConversation.user_id == current_user.id,
            AIConversation.context_type == request.context_type,
            AIConversation.context_id == request.context_id
        ).order_by(AIConversation.created_at.desc()).limit(5).all()
        
        # Reverse to get chronological order
        history = list(reversed(history))
        
        # Get AI response
        result = await ai_service.get_tutor_response(
            user_id=current_user.id,
            context_type=request.context_type,
            context_id=request.context_id,
            user_message=request.message,
            context_data=context_data,
            db=db,
            conversation_history=history
        )
        
        return ChatResponse(
            response=result["response"],
            tokens_used=result["tokens_used"],
            response_time_ms=result["response_time_ms"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI chat error for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service temporarily unavailable. Please try again."
        )


@router.post("/hint", response_model=HintResponse)
async def get_hint(
    request: HintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a progressive hint for a lab or challenge.
    Hint levels: 1=gentle nudge, 2=more specific, 3=direct guidance
    """
    try:
        # Validate context type (hints only for labs and challenges)
        if request.context_type not in ["lab", "challenge"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hints are only available for labs and challenges"
            )
        
        # Validate hint level
        if request.hint_level not in [1, 2, 3]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hint level must be 1, 2, or 3"
            )
        
        # Get context data
        context_data = get_context_data(request.context_type, request.context_id, db)
        
        # Generate hint
        hint = await ai_service.generate_hint(
            hint_level=request.hint_level,
            context_type=request.context_type,
            context_data=context_data
        )
        
        return HintResponse(
            hint=hint,
            level=request.hint_level
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Hint generation error for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate hint. Please try again."
        )


@router.get("/history/{context_type}/{context_id}")
async def get_conversation_history(
    context_type: str,
    context_id: int,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get conversation history for a specific context (lesson, lab, or challenge).
    Returns the most recent messages up to the limit.
    """
    try:
        # Validate context type
        if context_type not in ["lesson", "lab", "challenge"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid context type"
            )
        
        # Get conversation history
        conversations = db.query(AIConversation).filter(
            AIConversation.user_id == current_user.id,
            AIConversation.context_type == context_type,
            AIConversation.context_id == context_id
        ).order_by(AIConversation.created_at.desc()).limit(limit).all()
        
        # Reverse to get chronological order and format response
        result = []
        for conv in reversed(conversations):
            result.append({
                "id": conv.id,
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "created_at": conv.created_at.isoformat() if conv.created_at else None
            })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"History fetch error for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch conversation history"
        )


@router.delete("/history/{context_type}/{context_id}")
async def clear_conversation_history(
    context_type: str,
    context_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Clear conversation history for a specific context.
    """
    try:
        # Delete conversation history for this user and context
        deleted_count = db.query(AIConversation).filter(
            AIConversation.user_id == current_user.id,
            AIConversation.context_type == context_type,
            AIConversation.context_id == context_id
        ).delete()
        
        db.commit()
        
        return {"message": f"Cleared {deleted_count} messages", "deleted_count": deleted_count}
        
    except Exception as e:
        logger.error(f"History clear error for user {current_user.id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not clear conversation history"
        )
