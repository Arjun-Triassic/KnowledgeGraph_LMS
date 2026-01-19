import csv
import io
from typing import AsyncGenerator, List, Tuple

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.course import Course
from app.core.models.enrollment import Enrollment
from app.core.models.user import User
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate


class EnrollmentService(BaseService[Enrollment]):
    """
    Business logic for enrollments, including CSV streaming.
    """

    model = Enrollment

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def enroll_user(self, payload: EnrollmentCreate, _current_user: User) -> Enrollment:
        # Ensure user and course exist
        user = await self.session.get(User, payload.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        course = await self.session.get(Course, payload.course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course not found")

        # Avoid duplicate enrollment
        stmt = select(Enrollment).where(
            Enrollment.user_id == payload.user_id,
            Enrollment.course_id == payload.course_id,
        )
        existing = await self.session.execute(stmt)
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already enrolled",
            )

        return await self.create(payload.dict())

    async def list_enrollments(self, offset: int = 0, limit: int = 100) -> List[Enrollment]:
        return await self.list(offset=offset, limit=limit)

    async def update_enrollment(self, enrollment_id: int, payload: EnrollmentUpdate) -> Enrollment:
        enrollment = await self.get_by_id(enrollment_id)
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found",
            )
        return await self.update(enrollment, payload.dict(exclude_unset=True))

    async def stream_enrollments_csv(self) -> AsyncGenerator[str, None]:
        """
        Async generator that streams enrollments as CSV rows.
        """

        header = "user_id,course_id,progress,completion_percentage\n"
        yield header

        stmt = select(Enrollment)
        result = await self.session.stream(stmt)
        async for row in result.scalars():
            line = (
                f"{row.user_id},{row.course_id},"
                f"{row.progress},{row.completion_percentage}\n"
            )
            yield line

    async def import_enrollments_csv(
        self, file: UploadFile, batch_size: int = 1000
    ) -> Tuple[int, int, List[str]]:
        """
        Import enrollments from CSV file using async file reading and batch inserts.
        
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
                user_id = int(row.get("user_id", "").strip())
                course_id = int(row.get("course_id", "").strip())
                progress = float(row.get("progress", "0.0").strip() or "0.0")
                completion_percentage = float(
                    row.get("completion_percentage", "0.0").strip() or "0.0"
                )

                # Validate user and course exist
                user = await self.session.get(User, user_id)
                if not user:
                    raise ValueError(f"User {user_id} not found")

                course = await self.session.get(Course, course_id)
                if not course:
                    raise ValueError(f"Course {course_id} not found")

                # Check for duplicate enrollment
                stmt = select(Enrollment).where(
                    Enrollment.user_id == user_id, Enrollment.course_id == course_id
                )
                existing = await self.session.execute(stmt)
                if existing.scalar_one_or_none():
                    raise ValueError(f"User {user_id} already enrolled in course {course_id}")

                # Add to batch
                enrollment_data = {
                    "user_id": user_id,
                    "course_id": course_id,
                    "progress": progress,
                    "completion_percentage": completion_percentage,
                }
                batch.append(enrollment_data)

                # Insert batch when it reaches batch_size
                if len(batch) >= batch_size:
                    await self._bulk_insert_enrollments(batch)
                    success_count += len(batch)
                    batch = []

            except Exception as e:
                error_count += 1
                error_msg = f"Row {row_num}: {str(e)}"
                error_messages.append(error_msg)

        # Insert remaining batch
        if batch:
            await self._bulk_insert_enrollments(batch)
            success_count += len(batch)

        return success_count, error_count, error_messages

    async def _bulk_insert_enrollments(self, batch: List[dict]) -> None:
        """Helper method to bulk insert enrollments."""
        enrollments = [Enrollment(**data) for data in batch]
        self.session.add_all(enrollments)
        await self.session.commit()



