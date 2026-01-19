from __future__ import annotations

from typing import Callable, Iterable, Optional

from fastapi import Depends, HTTPException, status

from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user


def get_permission_checker(
    feature: str,
    action: str,
    resource: str,
    allowed_roles: Optional[Iterable[UserRole]] = None,
) -> Callable[[User], None]:
    """
    Dependency factory used by routes to express permissions in a declarative way.

    ``allowed_roles`` is an optional iterable of roles that may perform the action.
    If omitted, any authenticated user is allowed.
    """

    allowed = set(allowed_roles or [])

    async def checker(user: User = Depends(get_current_user)) -> None:
        if allowed and user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions for {feature}:{action}:{resource}",
            )

    return checker



