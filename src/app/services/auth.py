"""
Authentication service for the Taller Challenge API.
Handles password hashing, verification, JWT tokens, and authentication.
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.auth import User
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


class AuthService:
    """Service for handling authentication operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_admin_user(session: Session) -> User:
        """
        Create the default admin user with username 'admin' and password '1234'.
        """
        existing_user = session.exec(
            select(User).where(User.username == "admin")
        ).first()
        
        if existing_user:
            return existing_user

        hashed_password = AuthService.hash_password("1234")
        admin_user = User(
            username="admin",
            hashed_password=hashed_password
        )

        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)

        return admin_user

    @staticmethod
    def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = session.exec(
            select(User).where(User.username == username)
        ).first()

        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    async def authenticate_user_async(session, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password (async version)."""
        from sqlalchemy import select as sql_select

        result = await session.execute(
            sql_select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    async def get_current_user(session, token: str) -> Optional[User]:
        """Get current user from JWT token."""
        from sqlalchemy import select as sql_select

        payload = AuthService.verify_token(token)
        if not payload:
            return None

        username: str = payload.get("sub")
        if not username:
            return None

        result = await session.execute(
            sql_select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        return user


async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    This will be used to protect endpoints.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # I import here to avoid circular imports
    from app.core.db.database import get_db

    async for session in get_db():
        user = await AuthService.get_current_user(session, credentials.credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database connection error"
    )