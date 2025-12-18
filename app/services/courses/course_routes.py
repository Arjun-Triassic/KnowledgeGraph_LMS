from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.models.course import Course, course_prerequisite
from app.core.models.enums import UserRole
from app.core.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.roles import get_permission_checker
from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseSetPrerequisitesRequest,
    CourseUpdate,
)
from app.services.courses.course_service import CourseService


async def get_prerequisite_ids(session: AsyncSession, course_id: int) -> List[int]:
    """Helper to safely get prerequisite course IDs."""
    stmt = select(course_prerequisite.c.prereq_course_id).where(
        course_prerequisite.c.course_id == course_id
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


router = APIRouter()


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create course",
)
async def create_course(
    payload: CourseCreate,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Course Management",
            "create",
            "course",
            allowed_roles=[UserRole.ADMIN, UserRole.INSTRUCTOR],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    course = await service.create_course(payload, current_user)
    prerequisite_ids = await get_prerequisite_ids(session, course.id)
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        instructor_id=course.instructor_id,
        prerequisite_ids=prerequisite_ids,
    )


@router.get(
    "/",
    response_model=List[CourseResponse],
    summary="List courses",
)
async def list_courses(
    offset: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    courses = await service.list_courses(offset=offset, limit=limit)
    responses = []
    for course in courses:
        prerequisite_ids = await get_prerequisite_ids(session, course.id)
        responses.append(
            CourseResponse(
                id=course.id,
                title=course.title,
                description=course.description,
                category=course.category,
                instructor_id=course.instructor_id,
                prerequisite_ids=prerequisite_ids,
            )
        )
    return responses


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Get course by id",
)
async def get_course(
    course_id: int,
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    course = await service.get_course(course_id)
    prerequisite_ids = await get_prerequisite_ids(session, course.id)
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        instructor_id=course.instructor_id,
        prerequisite_ids=prerequisite_ids,
    )


@router.put(
    "/{course_id}",
    response_model=CourseResponse,
    summary="Update course",
)
async def update_course(
    course_id: int,
    payload: CourseUpdate,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Course Management",
            "update",
            "course",
            allowed_roles=[UserRole.ADMIN, UserRole.INSTRUCTOR],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    course = await service.update_course(course_id, payload, current_user)
    prerequisite_ids = await get_prerequisite_ids(session, course.id)
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        instructor_id=course.instructor_id,
        prerequisite_ids=prerequisite_ids,
    )


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete course",
)
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Course Management",
            "delete",
            "course",
            allowed_roles=[UserRole.ADMIN],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    await service.delete_course(course_id, current_user)


@router.post(
    "/{course_id}/assign-instructor/{instructor_id}",
    response_model=CourseResponse,
    summary="Assign instructor to course",
)
async def assign_instructor(
    course_id: int,
    instructor_id: int,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Course Management",
            "assign_instructor",
            "course",
            allowed_roles=[UserRole.ADMIN],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    course = await service.assign_instructor(course_id, instructor_id, current_user)
    prerequisite_ids = await get_prerequisite_ids(session, course.id)
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        instructor_id=course.instructor_id,
        prerequisite_ids=prerequisite_ids,
    )


@router.post(
    "/{course_id}/prerequisites",
    response_model=CourseResponse,
    summary="Set course prerequisites",
)
async def set_prerequisites(
    course_id: int,
    payload: CourseSetPrerequisitesRequest,
    current_user: User = Depends(get_current_user),
    _permissions=Depends(
        get_permission_checker(
            "Course Management",
            "set_prerequisites",
            "course",
            allowed_roles=[UserRole.ADMIN, UserRole.INSTRUCTOR],
        )
    ),
    session: AsyncSession = Depends(get_db_session),
):
    service = CourseService(session)
    course = await service.set_prerequisites(course_id, payload, current_user)
    prerequisite_ids = await get_prerequisite_ids(session, course.id)
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        category=course.category,
        instructor_id=course.instructor_id,
        prerequisite_ids=prerequisite_ids,
    )



