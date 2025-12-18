from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.assessment import Assessment, Option, Question
from app.core.models.user import User
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate, QuestionCreate


class AssessmentService(BaseService[Assessment]):
    """
    Business logic for assessments and questions.
    """

    model = Assessment

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_assessment(self, payload: AssessmentCreate, _current_user: User) -> Assessment:
        return await self.create(payload.dict())

    async def get_assessment(self, assessment_id: int) -> Assessment:
        assessment = await self.get_by_id(assessment_id)
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found",
            )
        return assessment

    async def update_assessment(self, assessment_id: int, payload: AssessmentUpdate) -> Assessment:
        assessment = await self.get_assessment(assessment_id)
        return await self.update(assessment, payload.dict(exclude_unset=True))

    async def add_question(
        self,
        assessment_id: int,
        payload: QuestionCreate,
        _current_user: User,
    ) -> Question:
        assessment = await self.get_assessment(assessment_id)
        question = Question(assessment_id=assessment.id, content=payload.content)
        self.session.add(question)
        await self.session.flush()

        for option_payload in payload.options:
            option = Option(
                question_id=question.id,
                text=option_payload.text,
                is_correct=option_payload.is_correct,
            )
            self.session.add(option)

        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def list_assessments_for_course(self, course_id: int) -> List[Assessment]:
        return await self.list(filters={"course_id": course_id})



