from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

STATUS_CREATED = 0
STATUS_PENDING_CHANGES = -1
STATUS_APPROVED = 1


class Note(Base):
    __tablename__ = "notes"
    _user_back_populates = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=False,
        nullable=False,
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id},text={self.text},created_at={self.created_at})"
        )

    def __repr__(self) -> str:
        return str(self)
