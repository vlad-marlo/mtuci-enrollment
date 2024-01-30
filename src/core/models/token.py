from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from . import Base


class Token(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=False,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String(20))
