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


@router.post(
    "/login", 
    response_model=LoginResponse,
    summary="Login to get JWT token",
    description="""
    **Step 1**: Use this endpoint to get your JWT token for authentication.
    
    **Default credentials:**
    - Username: `admin`
    - Password: `1234`
    
    **Response**: Contains `access_token` that you'll use for protected endpoints.
    
    **Next step**: Copy the `access_token` and use it in the 'Authorize' button above.
    """
)
async def login(
    login_data: LoginRequest,
    session = Depends(get_db)
):
    """
    Login endpoint to authenticate user credentials and get JWT token.
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


@router.get(
    "/me", 
    response_model=UserResponse,
    summary="Get current user info (Protected)",
    description="""
    **Protected Endpoint** - Requires JWT token authentication.
    
    This endpoint returns information about the currently authenticated user.
    
    **How to use:**
    1. First login via `/auth/login` to get your JWT token
    2. Click the 🔒 **Authorize** button and paste your token
    3. Then call this endpoint to verify your authentication is working
    """
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Get current authenticated user information (requires valid JWT token).
    """
    return UserResponse(id=current_user.id, username=current_user.username)