from typing import Optional

from pydantic import BaseModel


class LessonBase(BaseModel):
    name: str
    content_type: str


class LessonCreate(LessonBase):
    module_id: int


class LessonUpdate(BaseModel):
    name: Optional[str] = None
    content_type: Optional[str] = None


class LessonResponse(LessonBase):
    id: int
    module_id: int

    class Config:
        orm_mode = True



