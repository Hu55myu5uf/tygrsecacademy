"""
Pydantic Schemas for API Request/Response Models
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from models.user import UserRole


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.STUDENT


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    date_of_birth: Optional[str] = None  # Will be parsed as date
    country: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None


class UserResponse(UserBase):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    bio: Optional[str]
    avatar_url: Optional[str]
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    country: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class PublicProfileResponse(BaseModel):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    role: UserRole
    created_at: datetime
    
    # Gamification Stats
    current_tier: int = 0
    total_points: int = 0
    achievements: list[dict] = []
    
    class Config:
        from_attributes = True


# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


# Curriculum Schemas
class ContentBlockBase(BaseModel):
    type: str
    order: int
    text_content: Optional[str] = None
    code_content: Optional[str] = None
    code_language: Optional[str] = None
    media_url: Optional[str] = None
    quiz_data: Optional[str] = None


class ContentBlockCreate(ContentBlockBase):
    pass


class ContentBlockResponse(ContentBlockBase):
    id: int
    lesson_id: int
    
    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    content_markdown: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty: Optional[str] = "beginner"
    is_published: bool = False


class LessonCreate(LessonBase):
    pass


class LessonResponse(LessonBase):
    id: int
    module_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    content_blocks: list[ContentBlockResponse] = []
    challenge_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    estimated_hours: Optional[int] = None
    prerequisites: Optional[str] = None
    is_published: bool = False


class ModuleCreate(ModuleBase):
    pass


class ModuleResponse(ModuleBase):
    id: int
    tier_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    lessons: list[LessonResponse] = []
    
    class Config:
        from_attributes = True


class TierBase(BaseModel):
    tier_number: int
    name: str
    description: Optional[str] = None
    order: int
    is_active: bool = True


class TierCreate(TierBase):
    pass


class TierResponse(TierBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    modules: list[ModuleResponse] = []
    
    class Config:
        from_attributes = True


# Capstone Schemas
from typing import Any, Dict, List


class CapstoneTierBase(BaseModel):
    tier_id: int
    title: str
    description: str
    requirements: str  # Markdown
    deliverables: List[str]  # List of required items
    rubric: Dict[str, Any]  # Grading criteria
    max_score: int = 100
    passing_score: int = 70
    time_limit_hours: Optional[int] = None


class CapstoneTierCreate(CapstoneTierBase):
    pass


class CapstoneTierUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    deliverables: Optional[List[str]] = None
    rubric: Optional[Dict[str, Any]] = None
    max_score: Optional[int] = None
    passing_score: Optional[int] = None
    time_limit_hours: Optional[int] = None
    is_active: Optional[bool] = None


class CapstoneTierResponse(CapstoneTierBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class CapstoneSubmissionBase(BaseModel):
    github_url: Optional[str] = None
    documentation_url: Optional[str] = None
    demo_url: Optional[str] = None
    video_url: Optional[str] = None
    write_up: Optional[str] = None  # Markdown
    files_json: Optional[Dict[str, Any]] = None


class CapstoneSubmissionCreate(CapstoneSubmissionBase):
    capstone_tier_id: int


class CapstoneSubmissionUpdate(CapstoneSubmissionBase):
    pass


class CapstoneSubmissionResponse(CapstoneSubmissionBase):
    id: int
    user_id: int
    capstone_tier_id: int
    status: str
    submitted_at: Optional[datetime]
    started_at: datetime
    score: Optional[int]
    feedback: Optional[str]
    graded_by: Optional[int]
    graded_at: Optional[datetime]
    rubric_evaluation: Optional[Dict[str, Any]]
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Include related data
    capstone_tier_title: Optional[str] = None
    user_username: Optional[str] = None
    grader_username: Optional[str] = None
    
    class Config:
        from_attributes = True


class CapstoneGradeRequest(BaseModel):
    score: int = Field(..., ge=0, le=100)
    feedback: str
    rubric_evaluation: Optional[Dict[str, Any]] = None
    status: str = Field(..., pattern="^(graded|approved|rejected)$")


class CapstoneFeatureRequest(BaseModel):
    is_featured: bool
