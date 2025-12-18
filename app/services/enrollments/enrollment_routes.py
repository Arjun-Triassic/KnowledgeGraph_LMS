from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate
from app.services.enrollments.enrollment_service import EnrollmentService


router = APIRouter()


@router.post(
    "/",
    response_model=EnrollmentResponse,
    summary="Enroll user into a course",
)
async def enroll_user(
    payload: EnrollmentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> EnrollmentResponse:
    service = EnrollmentService(session)
    enrollment = await service.enroll_user(payload, current_user)
    return EnrollmentResponse.from_orm(enrollment)


@router.get(
    "/",
    response_model=List[EnrollmentResponse],
    summary="List enrollments",
)
async def list_enrollments(
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> List[EnrollmentResponse]:
    service = EnrollmentService(session)
    enrollments = await service.list_enrollments()
    return [EnrollmentResponse.from_orm(e) for e in enrollments]


@router.get(
    "/export",
    summary="Export enrollments as streaming CSV",
)
async def export_enrollments_csv(
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> StreamingResponse:
    service = EnrollmentService(session)
    generator = service.stream_enrollments_csv()
    return StreamingResponse(generator, media_type="text/csv")



