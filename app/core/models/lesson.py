from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.models.enums import LessonActivityType
from sqlalchemy import Enum


class Lesson(Base):
    """
    Individual lesson within a module.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("module.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)

    module: Mapped["Module"] = relationship("Module", back_populates="lessons")

    resources: Mapped[List["LessonResource"]] = relationship(
        "LessonResource",
        back_populates="lesson",
        cascade="all,delete-orphan",
    )

    activities: Mapped[List["LessonActivity"]] = relationship(
        "LessonActivity",
        back_populates="lesson",
        cascade="all,delete-orphan",
    )


class LessonResource(Base):
    """
    Static resource associated with a lesson (e.g. file, link).
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lesson.id", ondelete="CASCADE"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="resources")


class LessonActivity(Base):
    """
    Activity within a lesson: quiz, assignment, or project.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lesson.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[LessonActivityType] = mapped_column(
        Enum(LessonActivityType, name="lesson_activity_type"), nullable=False
    )

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="activities")

    questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="lesson_activity",
        cascade="all,delete-orphan",
    )

    submissions: Mapped[List["Submission"]] = relationship(
        "Submission",
        back_populates="lesson_activity",
        cascade="all,delete-orphan",
    )



