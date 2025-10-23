"""
Authentication models for the Taller Challenge API.
"""
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """
    User model for authentication.
    Simple model with just username and hashed password.
    """
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    hashed_password: str = Field(max_length=255)