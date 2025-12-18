from typing import Optional

from pydantic import BaseModel


class ModuleBase(BaseModel):
    name: str
    weight: float = 1.0


class ModuleCreate(ModuleBase):
    course_id: int


class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = None


class ModuleResponse(ModuleBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True



