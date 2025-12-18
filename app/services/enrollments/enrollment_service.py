from typing import AsyncGenerator, List

from fastapi import HTTPException, status
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

        header = "id,user_id,course_id,progress,completion_percentage,last_accessed\n"
        yield header

        stmt = select(Enrollment)
        result = await self.session.stream(stmt)
        async for row in result.scalars():
            last_accessed = (
                row.last_accessed.isoformat() if row.last_accessed is not None else ""
            )
            line = (
                f"{row.id},{row.user_id},{row.course_id},"
                f"{row.progress},{row.completion_percentage},{last_accessed}\n"
            )
            yield line



