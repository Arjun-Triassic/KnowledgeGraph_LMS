from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.models.enums import UserRole


class User(Base):
    """
    Application user with role-based access.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # Relationships
    courses_as_instructor: Mapped[List["Course"]] = relationship(
        "Course",
        back_populates="instructor",
        cascade="all,delete-orphan",
    )

    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="user",
        cascade="all,delete-orphan",
    )

    submissions: Mapped[List["Submission"]] = relationship(
        "Submission",
        back_populates="user",
        cascade="all,delete-orphan",
    )

    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
    )



