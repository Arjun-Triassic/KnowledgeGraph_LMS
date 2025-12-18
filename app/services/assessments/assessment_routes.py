from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import get_permission_checker
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentUpdate,
    QuestionCreate,
    QuestionResponse,
)
from app.services.assessments.assessment_service import AssessmentService


router = APIRouter()


@router.post(
    "/",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create assessment",
)
async def create_assessment(
    payload: AssessmentCreate,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Assessment Management",
            "create",
            "assessment",
            allowed_roles=[UserRole.ADMIN, UserRole.INSTRUCTOR],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
) -> AssessmentResponse:
    service = AssessmentService(session)
    assessment = await service.create_assessment(payload, current_user)
    return AssessmentResponse.from_orm(assessment)


@router.post(
    "/{assessment_id}/questions",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add question to assessment",
)
async def add_question(
    assessment_id: int,
    payload: QuestionCreate,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Assessment Management",
            "add_question",
            "assessment",
            allowed_roles=[UserRole.ADMIN, UserRole.INSTRUCTOR],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
) -> QuestionResponse:
    service = AssessmentService(session)
    question = await service.add_question(assessment_id, payload, current_user)
    return QuestionResponse.from_orm(question)


@router.get(
    "/by-course/{course_id}",
    response_model=List[AssessmentResponse],
    summary="List assessments for a course",
)
async def list_assessments_for_course(
    course_id: int,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> List[AssessmentResponse]:
    service = AssessmentService(session)
    assessments = await service.list_assessments_for_course(course_id)
    return [AssessmentResponse.from_orm(a) for a in assessments]



