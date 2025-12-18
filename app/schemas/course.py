from typing import List, Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: str
    category: str


class CourseCreate(CourseBase):
    instructor_id: Optional[int] = None


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    instructor_id: Optional[int] = None


class CourseResponse(CourseBase):
    id: int
    instructor_id: Optional[int]
    prerequisite_ids: List[int] = []

    class Config:
        orm_mode = True


class CourseSetPrerequisitesRequest(BaseModel):
    prerequisite_ids: List[int]



