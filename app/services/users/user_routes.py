from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import get_permission_checker
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.users.user_service import UserService


router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The created user",
)
async def create_user(
    payload: UserCreate,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "User Management",
            "create",
            "user",
            allowed_roles=[UserRole.ADMIN],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    service = UserService(session)
    return await service.create_user(payload, current_user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List users",
)
async def list_users(
    offset: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> List[User]:
    service = UserService(session)
    return await service.list_users(offset=offset, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by id",
)
async def get_user(
    user_id: int,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    service = UserService(session)
    return await service.get_user(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "User Management",
            "update",
            "user",
            allowed_roles=[UserRole.ADMIN],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    service = UserService(session)
    return await service.update_user(user_id, payload, current_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "User Management",
            "delete",
            "user",
            allowed_roles=[UserRole.ADMIN],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    service = UserService(session)
    await service.delete_user(user_id, current_user)



