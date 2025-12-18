from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.services.lessons.lesson_service import LessonService


router = APIRouter()


@router.post(
    "/",
    response_model=LessonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create lesson",
)
async def create_lesson(
    payload: LessonCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> LessonResponse:
    service = LessonService(session)
    lesson = await service.create_lesson(payload, current_user)
    return LessonResponse.from_orm(lesson)


@router.get(
    "/by-module/{module_id}",
    response_model=List[LessonResponse],
    summary="List lessons by module",
)
async def list_lessons_by_module(
    module_id: int,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> List[LessonResponse]:
    service = LessonService(session)
    lessons = await service.list_by_module(module_id)
    return [LessonResponse.from_orm(l) for l in lessons]



