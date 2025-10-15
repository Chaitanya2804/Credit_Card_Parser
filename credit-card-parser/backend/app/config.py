"""
Application configuration
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str = "postgresql://parser:parser123@db:5432/credit_parser"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list = [".pdf"]
    
    # Parser
    OCR_ENABLED: bool = True
    OCR_DPI: int = 300
    MAX_PAGES_OCR: int = 3
    
    # Security
    CORS_ORIGINS: list = ["http://localhost:3000", "http://frontend:3000"]
    
    class Config:
        env_file = ".env"


settings = Settings()