from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import get_permission_checker
from app.schemas.submission import (
    GradeSubmissionRequest,
    SubmissionCreate,
    SubmissionResponse,
)
from app.services.submissions.submission_service import SubmissionService


router = APIRouter()


@router.post(
    "/",
    response_model=SubmissionResponse,
    summary="Submit assignment or assessment",
)
async def submit(
    payload: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> SubmissionResponse:
    service = SubmissionService(session)
    submission = await service.submit(payload, current_user)
    return SubmissionResponse.from_orm(submission)


@router.post(
    "/{submission_id}/grade",
    response_model=SubmissionResponse,
    summary="Grade submission",
)
async def grade_submission(
    submission_id: int,
    payload: GradeSubmissionRequest,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Submission Management",
            "grade",
            "submission",
            allowed_roles=[UserRole.ADMIN, UserRole.INSTRUCTOR],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
) -> SubmissionResponse:
    service = SubmissionService(session)
    submission = await service.grade_submission(submission_id, payload, current_user)
    return SubmissionResponse.from_orm(submission)



