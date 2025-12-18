from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.core.models.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True



