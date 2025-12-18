from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.user import User


async def get_current_user(
    session: AsyncSession = Depends(get_db_session),
    x_user_id: Optional[int] = Header(default=None, alias="X-User-Id"),
) -> User:
    """
    Simple authentication dependency.

    In a real system this would be backed by JWTs or session tokens. For this
    project we keep it minimal and identify the user by ``X-User-Id`` header.
    """

    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id header required",
        )

    user = await session.get(User, x_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user



