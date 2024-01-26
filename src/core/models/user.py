from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from .database import Base

if TYPE_CHECKING:
    from .note import Note
    from .revision import Revision


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    middle_name: Mapped[str]
    last_name: Mapped[str]
    position: Mapped[str]
    can_check: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    revisions: Mapped[list["Revision"]] = relationship(back_populates="user")
