from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.decorators import role_required, validate_csv_headers
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate
from app.services.enrollments.enrollment_service import EnrollmentService
from app.services.email import (
    EmailService,
    ENROLLMENT_NOTIFICATION_TEMPLATE,
)


router = APIRouter()


async def send_enrollment_email_async(user_email: str, user_name: str, course_title: str):
    """Background task to send enrollment notification email."""
    email_service = EmailService()
    await email_service.send_email_from_template(
        to_email=user_email,
        subject=f"Welcome to {course_title}!",
        template_string=ENROLLMENT_NOTIFICATION_TEMPLATE,
        template_vars={
            "user_name": user_name,
            "course_title": course_title,
        },
    )


@router.post(
    "/",
    response_model=EnrollmentResponse,
    summary="Enroll user into a course",
)
async def enroll_user(
    payload: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> EnrollmentResponse:
    service = EnrollmentService(session)
    enrollment = await service.enroll_user(payload, current_user)
    
    # Send email notification in background
    from app.core.models.course import Course
    user = await session.get(User, enrollment.user_id)
    course = await session.get(Course, enrollment.course_id)
    if user and course:
        user_name = f"{user.first_name} {user.last_name}"
        background_tasks.add_task(
            send_enrollment_email_async,
            user.email,
            user_name,
            course.title,
        )
    
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


@router.post(
    "/import",
    summary="Import enrollments from CSV file",
    status_code=status.HTTP_200_OK,
)
async def import_enrollments_csv(
    file: UploadFile = Depends(
        validate_csv_headers(["user_id", "course_id", "progress", "completion_percentage"])
    ),
    current_user: User = Depends(role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    session: AsyncSession = Depends(get_db_session),
    batch_size: int = 1000,
) -> JSONResponse:
    """
    Import enrollments from CSV file.
    CSV format: user_id,course_id,progress,completion_percentage
    """
    service = EnrollmentService(session)
    success_count, error_count, error_messages = await service.import_enrollments_csv(
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



