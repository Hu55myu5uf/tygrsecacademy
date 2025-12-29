"""
Publishing Routes
Endpoints for capstone projects and blog publishing
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database.connection import get_db
from models.user import User, UserRole
from models.publishing import Capstone, BlogPost, CapstoneStatus, ExternalShare
from auth.rbac import get_current_user, require_tutor, require_admin

router = APIRouter()


# Capstone endpoints
@router.post("/capstone", response_model=dict)
async def submit_capstone(
    capstone_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a new capstone project"""
    capstone = Capstone(
        user_id=current_user.id,
        title=capstone_data['title'],
        description=capstone_data.get('description'),
        content_markdown=capstone_data.get('content_markdown'),
        files_url=capstone_data.get('files_url'),
        status=CapstoneStatus.SUBMITTED,
        submitted_at=datetime.utcnow()
    )
    db.add(capstone)
    db.commit()
    db.refresh(capstone)
    return {"id": capstone.id, "message": "Capstone submitted successfully"}


@router.get("/capstones", response_model=List[dict])
async def get_capstones(
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get capstones (filtered by status and user role)"""
    query = db.query(Capstone)
    
    # Students see only their own
    if current_user.role == UserRole.STUDENT:
        query = query.filter(Capstone.user_id == current_user.id)
    # Tutors see assigned + published
    elif current_user.role == UserRole.TUTOR:
        query = query.filter(
            (Capstone.tutor_id == current_user.id) | 
            (Capstone.status == CapstoneStatus.PUBLISHED)
        )
    # Admins see all
    
    if status_filter:
        query = query.filter(Capstone.status == status_filter)
    
    capstones = query.all()
    
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "status": c.status,
            "score": c.score,
            "submitted_at": c.submitted_at.isoformat() if c.submitted_at else None,
            "author_id": c.user_id
        }
        for c in capstones
    ]


@router.get("/capstones/{capstone_id}", response_model=dict)
async def get_capstone(
    capstone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific capstone details"""
    capstone = db.query(Capstone).filter(Capstone.id == capstone_id).first()
    if not capstone:
        raise HTTPException(status_code=404, detail="Capstone not found")
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and capstone.user_id != current_user.id:
        if capstone.status != CapstoneStatus.PUBLISHED:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "id": capstone.id,
        "title": capstone.title,
        "description": capstone.description,
        "content_markdown": capstone.content_markdown,
        "files_url": capstone.files_url,
        "status": capstone.status,
        "tutor_feedback": capstone.tutor_feedback,
        "score": capstone.score,
        "submitted_at": capstone.submitted_at.isoformat() if capstone.submitted_at else None
    }


@router.put("/capstones/{capstone_id}/review", dependencies=[Depends(require_tutor)])
async def review_capstone(
    capstone_id: int,
    review_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Review a capstone (Tutor/Admin only)"""
    capstone = db.query(Capstone).filter(Capstone.id == capstone_id).first()
    if not capstone:
        raise HTTPException(status_code=404, detail="Capstone not found")
    
    capstone.tutor_feedback = review_data.get('feedback')
    capstone.score = review_data.get('score')
    capstone.status = CapstoneStatus.APPROVED if review_data.get('approved') else CapstoneStatus.REJECTED
    capstone.reviewed_at = datetime.utcnow()
    capstone.tutor_id = current_user.id
    
    db.commit()
    return {"message": "Review submitted"}


# Blog endpoints
@router.get("/blog", response_model=List[dict])
async def get_blog_posts(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get published blog posts"""
    posts = db.query(BlogPost).filter(
        BlogPost.is_published == True
    ).order_by(BlogPost.published_at.desc()).limit(limit).all()
    
    return [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "summary": p.summary,
            "cover_image_url": p.cover_image_url,
            "author_id": p.author_id,
            "tags": p.tags,
            "views_count": p.views_count,
            "likes_count": p.likes_count,
            "published_at": p.published_at.isoformat() if p.published_at else None
        }
        for p in posts
    ]


@router.get("/blog/{slug}", response_model=dict)
async def get_blog_post(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get specific blog post by slug"""
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post or not post.is_published:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Increment views
    post.views_count += 1
    db.commit()
    
    return {
        "id": post.id,
        "title": post.title,
        "content_markdown": post.content_markdown,
        "cover_image_url": post.cover_image_url,
        "author_id": post.author_id,
        "tags": post.tags,
        "views_count": post.views_count,
        "likes_count": post.likes_count,
        "publishedAt": post.published_at.isoformat() if post.published_at else None
    }


@router.post("/blog", dependencies=[Depends(require_admin)])
async def publish_blog(
    blog_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Publish a new blog post (Admin only)"""
    post = BlogPost(
        author_id=current_user.id,
        title=blog_data['title'],
        slug=blog_data['slug'],
        summary=blog_data.get('summary'),
        content_markdown=blog_data['content_markdown'],
        cover_image_url=blog_data.get('cover_image_url'),
        tags=blog_data.get('tags'),
        is_published=True,
        published_at=datetime.utcnow()
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id, "slug": post.slug, "message": "Blog post published"}
