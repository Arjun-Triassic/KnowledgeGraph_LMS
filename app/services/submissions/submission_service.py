from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.assessment import Assessment
from app.core.models.lesson import LessonActivity
from app.core.models.submission import Submission
from app.core.models.user import User
from app.schemas.submission import GradeSubmissionRequest, SubmissionCreate


class SubmissionService(BaseService[Submission]):
    """
    Business logic for submissions and grading.
    """

    model = Submission

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def submit(self, payload: SubmissionCreate, current_user: User) -> Submission:
        if payload.assessment_id is None and payload.lesson_activity_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="assessment_id or lesson_activity_id is required",
            )

        if payload.assessment_id is not None:
            assessment = await self.session.get(Assessment, payload.assessment_id)
            if not assessment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assessment not found",
                )

        if payload.lesson_activity_id is not None:
            activity = await self.session.get(LessonActivity, payload.lesson_activity_id)
            if not activity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Lesson activity not found",
                )

        data = payload.dict()
        data["user_id"] = current_user.id
        return await self.create(data)

    async def grade_submission(
        self,
        submission_id: int,
        payload: GradeSubmissionRequest,
        _current_user: User,
    ) -> Submission:
        submission = await self.get_by_id(submission_id)
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found",
            )
        submission.score = payload.score
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)
        return submission



