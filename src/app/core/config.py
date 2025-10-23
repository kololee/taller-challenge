"""
Configuration settings for the Taller Challenge API.
This module handles environment variables and application settings.
"""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    DATABASE_URL: str = Field(
        description="PostgreSQL database URL",
        examples=["postgresql://user:password@localhost:5432/dbname"]
    )
    
    # API Configuration
    API_V1_STR: str = Field(default="/api/v1", description="API version 1 prefix")
    PROJECT_NAME: str = Field(default="Taller Challenge API", description="Project name")
    PROJECT_VERSION: str = Field(default="1.0.0", description="Project version")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # Authentication
    SECRET_KEY: str = Field(default="secret-key-for-taller-challenge-schmitt", description="Secret key for JWT tokens")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="JWT token expiration time in minutes")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"  # Ignore extra environment variables
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Global settings instance
settings = get_settings()