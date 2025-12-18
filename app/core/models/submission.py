from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base


class Submission(Base):
    """
    Submission for either an assessment or a lesson activity.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    assessment_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("assessment.id", ondelete="CASCADE"),
        nullable=True,
    )
    lesson_activity_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("lessonactivity.id", ondelete="CASCADE"),
        nullable=True,
    )
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="submissions")
    assessment: Mapped["Assessment | None"] = relationship(
        "Assessment",
        back_populates="submissions",
    )
    lesson_activity: Mapped["LessonActivity | None"] = relationship(
        "LessonActivity",
        back_populates="submissions",
    )



