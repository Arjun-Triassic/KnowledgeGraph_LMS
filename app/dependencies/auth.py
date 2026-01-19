from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import decode_access_token
from app.core.db.session import get_db_session
from app.core.models.user import User

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)


async def get_current_user(
    session: AsyncSession = Depends(get_db_session),
    x_user_id: Optional[int] = Header(default=None, alias="X-User-Id"),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> User:
    """
    Authentication dependency that supports both methods:
    1. X-User-Id header (backward compatible)
    2. Bearer token (JWT) from Authorization header
    
    Priority: Token authentication takes precedence if both are provided.
    """

    # Try token authentication first (if provided)
    if credentials:
        token = credentials.credentials
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                try:
                    user_id_int = int(user_id)
                    user = await session.get(User, user_id_int)
                    if user:
                        return user
                except (ValueError, TypeError):
                    pass

    # Fall back to header-based authentication (backward compatible)
    if x_user_id is not None:
        user = await session.get(User, x_user_id)
        if user:
            return user

    # If neither method works, raise error
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide either X-User-Id header or Bearer token.",
        headers={"WWW-Authenticate": "Bearer"},
    )



