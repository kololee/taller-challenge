"""
Authentication schemas for the Taller Challenge API.
Pydantic models for request/response validation.
"""
from pydantic import BaseModel


class UserResponse(BaseModel):
    """Response model for user data."""
    id: int
    username: str
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Request model for user login."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Response model for successful login."""
    access_token: str
    token_type: str
    user: UserResponse


class TokenResponse(BaseModel):
    """Response model for token operations."""
    access_token: str
    token_type: str