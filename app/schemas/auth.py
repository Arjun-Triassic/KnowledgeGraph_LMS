"""
Authentication schemas for login and registration.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from app.core.models.enums import UserRole


class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password (8-72 characters)")
    first_name: str
    last_name: str
    role: UserRole = UserRole.LEARNER  # Default role for new registrations

    @validator('password')
    def validate_password_length(cls, v):
        """Validate password length for bcrypt compatibility."""
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes when encoded')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=72, description="Password (max 72 bytes)")


class Token(BaseModel):
    """Schema for access token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    role: str


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: Optional[int] = None
    email: Optional[str] = None
