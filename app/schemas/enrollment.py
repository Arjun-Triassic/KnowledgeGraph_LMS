from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class EnrollmentUpdate(BaseModel):
    progress: Optional[float] = None
    completion_percentage: Optional[float] = None
    last_accessed: Optional[datetime] = None


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress: float
    completion_percentage: float
    last_accessed: Optional[datetime]

    class Config:
        orm_mode = True



