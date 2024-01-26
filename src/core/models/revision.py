from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Revision(Base):
    __tablename__ = "revisions"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
    )
    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id"),
        nullable=False,
    )
