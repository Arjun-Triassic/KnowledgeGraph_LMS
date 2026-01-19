import csv
import io
from typing import List, Tuple

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.lesson import Lesson
from app.core.models.module import Module
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

    async def import_lessons_csv(
        self, file: UploadFile, batch_size: int = 1000
    ) -> Tuple[int, int, List[str]]:
        """
        Import lessons from CSV file using async file reading and batch inserts.
        
        Expected CSV format:
        module_id,name,content_type
        
        Returns:
            Tuple of (success_count, error_count, error_messages)
        """
        success_count = 0
        error_count = 0
        error_messages = []
        batch = []

        # Read file asynchronously
        content = await file.read()
        text_content = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text_content))

        for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
            try:
                # Clean and validate data
                module_id = int(row.get("module_id", "").strip())
                name = row.get("name", "").strip()
                content_type = row.get("content_type", "").strip()

                if not name:
                    raise ValueError("Lesson name is required")
                if not content_type:
                    raise ValueError("Content type is required")

                # Validate module exists
                module = await self.session.get(Module, module_id)
                if not module:
                    raise ValueError(f"Module {module_id} not found")

                # Add to batch
                lesson_data = {
                    "module_id": module_id,
                    "name": name,
                    "content_type": content_type,
                }
                batch.append(lesson_data)

                # Insert batch when it reaches batch_size
                if len(batch) >= batch_size:
                    await self._bulk_insert_lessons(batch)
                    success_count += len(batch)
                    batch = []

            except Exception as e:
                error_count += 1
                error_msg = f"Row {row_num}: {str(e)}"
                error_messages.append(error_msg)

        # Insert remaining batch
        if batch:
            await self._bulk_insert_lessons(batch)
            success_count += len(batch)

        return success_count, error_count, error_messages

    async def _bulk_insert_lessons(self, batch: List[dict]) -> None:
        """Helper method to bulk insert lessons."""
        lessons = [Lesson(**data) for data in batch]
        self.session.add_all(lessons)
        await self.session.commit()



