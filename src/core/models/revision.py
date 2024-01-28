from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

if TYPE_CHECKING:
    from .user import User


class Revision(Base):
    __tablename__ = "revisions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
    )
    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id"),
        nullable=False,
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    passed: Mapped[bool]

    user: Mapped["User"] = relationship(
        "User",
        back_populates="revision",
    )
