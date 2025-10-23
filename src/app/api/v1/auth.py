"""
Authentication routes for the Taller Challenge API.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from app.services.auth import AuthService, get_current_user_dependency
from app.core.db.database import get_db
from app.models.auth import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    session = Depends(get_db)
):
    """
    Login endpoint to authenticate user credentials.
    Returns JWT access token and user information if credentials are valid.
    """
    user = await AuthService.authenticate_user_async(
        session=session,
        username=login_data.username,
        password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = AuthService.create_access_token(
        data={"sub": user.username}
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user.id, username=user.username)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Get current authenticated user information.
    This is a protected endpoint that requires a valid JWT token.
    """
    return UserResponse(id=current_user.id, username=current_user.username)