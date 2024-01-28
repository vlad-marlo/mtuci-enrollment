from sqlalchemy import select, and_, desc, false, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage.abs import BaseNotesStorage
from src.core.models import Note
from src.sync_decorator import with_lock

lock = with_lock()


class NotesStorage(BaseNotesStorage):
    def __init__(self, session: AsyncSession):
        self._session = session

    @lock
    async def create(self, note: Note) -> Note:
        """create stores note to system"""
        self._session.add(note)
        await self._session.commit()
        return note

    @lock
    async def update(self, note: Note) -> Note:
        """update updates note and returns changed Note to user"""
        pass

    @lock
    async def delete(self, note: Note) -> None:
        """deletes note"""
        stmt = update(Note).where(Note.id == note.id).values(is_deleted=True)
        await self._session.execute(stmt)
        return None

    @lock
    async def __get_by_stmt(self, stmt) -> list[Note]:
        result = await self._session.execute(stmt)
        notes = result.scalars().all()
        return list(notes)

    async def get_all_by_user_id_with_status(
            self,
            user_id: int,
            status: int,
    ) -> list[Note]:
        """
        return all notes, related to user with status.

        Status must be integer in absolute value less or equal to 1.
        """
        stmt = (
            select(Note)
            .where(
                and_(
                    Note.user_id == user_id,
                    Note.status == status,
                    not Note.is_deleted,
                ),
            ).order_by(desc(Note.created_at))
        )
        result = await self.__get_by_stmt(stmt)
        return result

    async def get_all_by_user_id(self, user_id: int) -> list[Note]:
        """return all notes, related to user with provided id"""
        stmt = (
            select(Note)
            .where(
                and_(
                    Note.user_id == user_id,
                    not Note.is_deleted,
                ),
            )
            .order_by(desc(Note.created_at))
        )
        result = await self.__get_by_stmt(stmt)
        return result
