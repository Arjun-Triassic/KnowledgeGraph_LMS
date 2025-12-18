from typing import List, Optional

from pydantic import BaseModel

from app.core.models.enums import AssessmentType


class AssessmentBase(BaseModel):
    course_id: int
    type: AssessmentType
    total_marks: float


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    type: Optional[AssessmentType] = None
    total_marks: Optional[float] = None


class AssessmentResponse(AssessmentBase):
    id: int

    class Config:
        orm_mode = True


class QuestionOptionCreate(BaseModel):
    text: str
    is_correct: bool = False


class QuestionCreate(BaseModel):
    content: str
    options: List[QuestionOptionCreate]


class QuestionResponse(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True



