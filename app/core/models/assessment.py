from typing import List, Optional

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.models.enums import AssessmentType


class Assessment(Base):
    """
    Assessment belonging to a course (exam or quiz).
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[AssessmentType] = mapped_column(
        Enum(AssessmentType, name="assessment_type"),
        nullable=False,
    )
    total_marks: Mapped[float] = mapped_column(Float, nullable=False)

    course: Mapped["Course"] = relationship("Course", back_populates="assessments")

    questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="assessment",
        cascade="all,delete-orphan",
    )

    submissions: Mapped[List["Submission"]] = relationship(
        "Submission",
        back_populates="assessment",
        cascade="all,delete-orphan",
    )


class Question(Base):
    """
    Question for an assessment or lesson activity.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assessment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("assessment.id", ondelete="CASCADE"),
        nullable=True,
    )
    lesson_activity_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("lessonactivity.id", ondelete="CASCADE"),
        nullable=True,
    )
    content: Mapped[str] = mapped_column(String(1000), nullable=False)

    assessment: Mapped[Optional["Assessment"]] = relationship(
        "Assessment",
        back_populates="questions",
    )

    lesson_activity: Mapped[Optional["LessonActivity"]] = relationship(
        "LessonActivity",
        back_populates="questions",
    )

    options: Mapped[List["Option"]] = relationship(
        "Option",
        back_populates="question",
        cascade="all,delete-orphan",
    )


class Option(Base):
    """
    Multiple-choice option for a question.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False
    )
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    text: Mapped[str] = mapped_column(String(500), nullable=False)

    question: Mapped["Question"] = relationship("Question", back_populates="options")



