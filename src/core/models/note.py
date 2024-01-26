from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base
from .mixins import UserMixin


class Note(Base, UserMixin):
    __tablename__ = "notes"
    _user_back_populates = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
