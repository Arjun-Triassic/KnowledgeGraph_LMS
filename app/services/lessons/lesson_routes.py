from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.decorators import role_required, validate_csv_headers
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


@router.post(
    "/import",
    summary="Import lessons from CSV file",
    status_code=status.HTTP_200_OK,
)
async def import_lessons_csv(
    file: UploadFile = Depends(validate_csv_headers(["module_id", "name", "content_type"])),
    current_user: User = Depends(role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    session: AsyncSession = Depends(get_db_session),
    batch_size: int = 1000,
) -> JSONResponse:
    """
    Import lessons from CSV file.
    CSV format: module_id,name,content_type
    """
    service = LessonService(session)
    success_count, error_count, error_messages = await service.import_lessons_csv(
        file, batch_size=batch_size
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success_count": success_count,
            "error_count": error_count,
            "errors": error_messages[:100],  # Limit to first 100 errors
            "message": f"Import completed: {success_count} successful, {error_count} errors",
        },
    )



