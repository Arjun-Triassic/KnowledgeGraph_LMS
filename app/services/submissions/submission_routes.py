from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.assessment import Assessment
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import get_permission_checker
from app.schemas.submission import (
    GradeSubmissionRequest,
    SubmissionCreate,
    SubmissionResponse,
)
from app.services.email import (
    EmailService,
    SUBMISSION_NOTIFICATION_TEMPLATE,
)
from app.services.submissions.submission_service import SubmissionService


router = APIRouter()


async def send_submission_notification_email_async(
    instructor_email: str,
    instructor_name: str,
    student_name: str,
    assessment_title: str,
    submission_date: str,
):
    """Background task to send submission notification email to instructor."""
    email_service = EmailService()
    await email_service.send_email_from_template(
        to_email=instructor_email,
        subject=f"New Submission: {assessment_title}",
        template_string=SUBMISSION_NOTIFICATION_TEMPLATE,
        template_vars={
            "instructor_name": instructor_name,
            "student_name": student_name,
            "assessment_title": assessment_title,
            "submission_date": submission_date,
        },
    )


@router.post(
    "/",
    response_model=SubmissionResponse,
    summary="Submit assignment or assessment",
)
async def submit(
    payload: SubmissionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> SubmissionResponse:
    service = SubmissionService(session)
    submission = await service.submit(payload, current_user)
    
    # Send email notification to instructor in background
    if submission.assessment_id:
        assessment = await session.get(Assessment, submission.assessment_id)
        if assessment and assessment.course:
            course = assessment.course
            if course.instructor_id:
                instructor = await session.get(User, course.instructor_id)
                if instructor:
                    student_name = f"{current_user.first_name} {current_user.last_name}"
                    instructor_name = f"{instructor.first_name} {instructor.last_name}"
                    assessment_title = f"Assessment for {course.title}"
                    submission_date = submission.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
                    
                    background_tasks.add_task(
                        send_submission_notification_email_async,
                        instructor.email,
                        instructor_name,
                        student_name,
                        assessment_title,
                        submission_date,
                    )
    
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



