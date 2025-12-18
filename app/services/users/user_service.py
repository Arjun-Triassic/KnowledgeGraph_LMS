from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService(BaseService[User]):
    """
    Business logic for user management.
    """

    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_user(self, payload: UserCreate, current_user: User) -> User:
        if current_user.role is not UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can create users",
            )

        existing = await self.session.execute(select(User).where(User.email == payload.email))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )

        return await self.create(payload.dict())

    async def list_users(self, offset: int = 0, limit: int = 100) -> List[User]:
        return await self.list(offset=offset, limit=limit)

    async def get_user(self, user_id: int) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_user(self, user_id: int, payload: UserUpdate, current_user: User) -> User:
        if current_user.role is not UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update users",
            )

        user = await self.get_user(user_id)
        return await self.update(user, payload.dict(exclude_unset=True))

    async def delete_user(self, user_id: int, current_user: User) -> None:
        if current_user.role is not UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can delete users",
            )

        user = await self.get_user(user_id)
        await self.delete(user)



