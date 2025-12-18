from typing import List

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.models.enums import AssessmentType


course_prerequisite = Table(
    "course_prerequisite",
    Base.metadata,
    Column("course_id", ForeignKey("course.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "prereq_course_id",
        ForeignKey("course.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Course(Base):
    """
    Top-level course entity.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)

    instructor_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )

    instructor: Mapped["User | None"] = relationship(
        "User",
        back_populates="courses_as_instructor",
    )

    modules: Mapped[List["Module"]] = relationship(
        "Module",
        back_populates="course",
        cascade="all,delete-orphan",
    )

    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="course",
        cascade="all,delete-orphan",
    )

    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all,delete-orphan",
    )

    # Self-referential many-to-many for prerequisites
    prerequisites: Mapped[List["Course"]] = relationship(
        "Course",
        secondary=course_prerequisite,
        primaryjoin=id == course_prerequisite.c.course_id,
        secondaryjoin=id == course_prerequisite.c.prereq_course_id,
        backref="dependents",
    )



