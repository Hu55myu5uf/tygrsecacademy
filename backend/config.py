"""
TygrSecAcademy Configuration
Manages all application configuration from environment variables
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "TygrSecAcademy"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str
    
    # Database
    DATABASE_URL: str
    DB_ECHO: bool = False
    
    # Redis
    REDIS_URL: str
    
    # JWT Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours (changed from 15 mins)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # Extended from 7 days
    
    # Password Security
    BCRYPT_COST_FACTOR: int = 12
    
    # Google Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_MAX_TOKENS: int = 4096
    
    # AI Configuration
    AI_CONTEXT_MAX_TOKENS: int = 16000
    AI_CACHE_TTL_SECONDS: int = 3600
    AI_RATE_LIMIT_PER_USER_PER_HOUR: int = 50
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: str = "pdf,png,jpg,jpeg,md,txt,py,js,html,css"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@tygrsecacademy.com"
    SMTP_FROM_NAME: str = "TygrSecAcademy"
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"
    
    # CORS Settings
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    AUTH_RATE_LIMIT_PER_MINUTE: int = 5
    
    # Lab Environment
    LAB_DOCKER_NETWORK: str = "tygrsec-lab-network"
    LAB_SESSION_TIMEOUT_MINUTES: int = 60
    LAB_MAX_CONCURRENT_PER_USER: int = 3
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/tygrsecacademy.log"
    
    # Security
    SECURE_COOKIES: bool = False
    HTTPS_REDIRECT: bool = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed file extensions into a list"""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
