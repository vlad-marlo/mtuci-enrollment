from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, validates

from .database import Base
from .mixins import UserMixin

STATUS_CREATED = 0
STATUS_PENDING_CHANGES = -1
STATUS_APPROVED = 1


class Note(Base, UserMixin):
    __tablename__ = "notes"
    _user_back_populates = "note"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    status: Mapped[int]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    @validates("status")
    def validate_status(self, key, status):
        if abs(status) > 1:
            raise ValueError("status must be 0 or 1 or -1")
        return status

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(id={self.id},text={self.text},created_at={self.created_at})"
        )

    def __repr__(self) -> str:
        return str(self)
