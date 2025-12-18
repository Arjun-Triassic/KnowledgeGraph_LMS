from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.module import ModuleCreate, ModuleResponse, ModuleUpdate
from app.services.modules.module_service import ModuleService


router = APIRouter()


@router.post(
    "/",
    response_model=ModuleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create module",
)
async def create_module(
    payload: ModuleCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> ModuleResponse:
    service = ModuleService(session)
    module = await service.create_module(payload, current_user)
    return ModuleResponse.from_orm(module)


@router.get(
    "/by-course/{course_id}",
    response_model=List[ModuleResponse],
    summary="List modules by course",
)
async def list_modules_by_course(
    course_id: int,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> List[ModuleResponse]:
    service = ModuleService(session)
    modules = await service.list_by_course(course_id)
    return [ModuleResponse.from_orm(m) for m in modules]



