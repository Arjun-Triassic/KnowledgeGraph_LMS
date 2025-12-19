from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.lesson import Lesson
from app.core.models.user import User
from app.schemas.lesson import LessonCreate, LessonUpdate


class LessonService(BaseService[Lesson]):
    """
    Business logic for lessons.
    """

    model = Lesson

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_lesson(self, payload: LessonCreate, _current_user: User) -> Lesson:
        return await self.create(payload.dict())

    async def list_by_module(self, module_id: int) -> List[Lesson]:
        return await self.list(filters={"module_id": module_id})

    async def get_lesson(self, lesson_id: int) -> Lesson:
        lesson = await self.get_by_id(lesson_id)
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
        return lesson


    async def update_lesson(self, lesson_id: int, payload: LessonUpdate) -> Lesson:
        lesson = await self.get_lesson(lesson_id)
        return await self.update(lesson, payload.dict(exclude_unset=True))



