from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.common.base_service import BaseService
from app.core.models.course import Course
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.schemas.course import CourseCreate, CourseSetPrerequisitesRequest, CourseUpdate


class CourseService(BaseService[Course]):
    """
    Business logic for courses, instructors, and prerequisites.
    """

    model = Course

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_course(self, payload: CourseCreate, current_user: User) -> Course:
        if current_user.role not in (UserRole.ADMIN, UserRole.INSTRUCTOR):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins or instructors can create courses",
            )
        return await self.create(payload.dict())

    async def update_course(self, course_id: int, payload: CourseUpdate, current_user: User) -> Course:
        course = await self.get_course(course_id)
        if current_user.role not in (UserRole.ADMIN, UserRole.INSTRUCTOR):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return await self.update(course, payload.dict(exclude_unset=True))

    async def delete_course(self, course_id: int, current_user: User) -> None:
        if current_user.role is not UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can delete courses",
            )
        course = await self.get_course(course_id)
        await self.delete(course)

    async def list_courses(self, offset: int = 0, limit: int = 100) -> List[Course]:
        return await self.list(offset=offset, limit=limit)

    async def get_course(self, course_id: int) -> Course:
        course = await self.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return course

    async def assign_instructor(self, course_id: int, instructor_id: int, current_user: User) -> Course:
        if current_user.role is not UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can assign instructors",
            )
        course = await self.get_course(course_id)
        # Ensure instructor exists and has correct role
        instructor = await self.session.get(User, instructor_id)
        if not instructor or instructor.role is not UserRole.INSTRUCTOR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Instructor not found or not an instructor",
            )
        course.instructor_id = instructor_id
        await self.session.commit()
        await self.session.refresh(course)
        return course

    async def set_prerequisites(
        self,
        course_id: int,
        payload: CourseSetPrerequisitesRequest,
        current_user: User,
    ) -> Course:
        if current_user.role not in (UserRole.ADMIN, UserRole.INSTRUCTOR):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        course = await self.get_course(course_id)

        if not payload.prerequisite_ids:
            course.prerequisites.clear()
            await self.session.commit()
            await self.session.refresh(course)
            return course

        stmt = select(Course).where(Course.id.in_(payload.prerequisite_ids))
        result = await self.session.execute(stmt)
        prereqs = result.scalars().all()

        if len(prereqs) != len(set(payload.prerequisite_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more prerequisite courses not found",
            )

        course.prerequisites = list(prereqs)
        await self.session.commit()
        await self.session.refresh(course)
        return course



