from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    user_id: int
    assessment_id: Optional[int] = None
    lesson_activity_id: Optional[int] = None
    score: Optional[float] = None


class GradeSubmissionRequest(BaseModel):
    score: float


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    assessment_id: Optional[int]
    lesson_activity_id: Optional[int]
    score: Optional[float]
    submitted_at: datetime

    class Config:
        orm_mode = True



