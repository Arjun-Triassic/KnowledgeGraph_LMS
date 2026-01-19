"""
Authentication service for user registration and login.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token, get_password_hash, verify_password
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.schemas.auth import UserLogin, UserRegister
from fastapi import HTTPException, status


class AuthService:
    """Service for authentication operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user(self, payload: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            payload: User registration data
            
        Returns:
            Created user object
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        stmt = select(User).where(User.email == payload.email)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        hashed_password = get_password_hash(payload.password)
        user_data = {
            "email": payload.email,
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "role": payload.role,
            "hashed_password": hashed_password,
        }
        
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user

    async def authenticate_user(self, payload: UserLogin) -> User:
        """
        Authenticate a user with email and password.
        
        Args:
            payload: User login credentials
            
        Returns:
            Authenticated user object
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        stmt = select(User).where(User.email == payload.email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        
        # Check if user has a password set (for backward compatibility)
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password not set for this user. Please contact administrator.",
            )
        
        # Verify password
        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        
        return user

    async def create_token_for_user(self, user: User) -> dict:
        """
        Create an access token for a user.
        
        Args:
            user: User object
            
        Returns:
            Dictionary with token data
        """
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
        }
