from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from . import Base

if TYPE_CHECKING:
    from .user import User


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=False,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String(20))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="tokens"
    )

    def __str__(self):
        return f"Token(id={self.id}, token={self.token})"
