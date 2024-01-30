from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from .database import Base

if TYPE_CHECKING:
    from .note import Note
    from .revision import Revision
    from .token import Token


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    middle_name: Mapped[str | None]
    last_name: Mapped[str]
    position: Mapped[str]
    can_check: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str]

    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    revisions: Mapped[list["Revision"]] = relationship(back_populates="user")
    tokens: Mapped[list["Token"]] = relationship(back_populates="user")

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id},"
            f"full_name={self.first_name + self.middle_name + self.last_name},"
            f"position={self.position},can_check={self.can_check})"
        )
