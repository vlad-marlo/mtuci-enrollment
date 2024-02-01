from sqlalchemy import select, and_, desc, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseNotesStorage
from src.core.models import Note


class NotesStorage(BaseNotesStorage):
    def __init__(self):
        return

    async def create(
            self,
            note: Note,
            *,
            session: AsyncSession,
    ) -> Note:
        """create stores note to system"""
        session.add(note)
        await session.commit()
        return note

    async def update(
            self,
            note: Note,
            *,
            session: AsyncSession,
            **kwargs,
    ) -> None:
        """update updates note and returns changed Note to user"""
        stmt = update(Note).where(Note.id == note.id).values(**kwargs)
        await session.execute(stmt)

    async def delete(
            self,
            note: Note,
            *,
            session: AsyncSession,
    ) -> None:
        """deletes note"""
        stmt = update(Note).where(Note.id == note.id).values(is_deleted=True)
        await session.execute(stmt)
        return None

    async def __get_by_stmt(
            self,
            stmt,
            *,
            session: AsyncSession,
    ) -> list[Note]:
        result = await session.execute(stmt)
        notes = result.scalars().all()
        return list(notes)

    async def get_all_by_user_id_and_passing(
            self,
            user_id: int,
            passed: bool,
            session: AsyncSession,
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
                    not Note.is_deleted,
                    Note.revision.passed == passed,
                ),
            ).order_by(desc(Note.created_at))
        )
        result = await self.__get_by_stmt(stmt, session=session)
        return result

    async def get_all_by_user_id(
            self,
            user_id: int,
            *,
            session: AsyncSession,
    ) -> list[Note]:
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
        result = await self.__get_by_stmt(stmt, session=session)
        return result

    async def get_all(self, session: AsyncSession) -> list[Note]:
        stmt = (
            select(Note)
            .where(
                not Note.is_deleted,

            )
            .order_by(desc(Note.created_at))
        )
        result = await self.__get_by_stmt(stmt, session=session)
        return result

    async def get_all_with_revisions(self, session: AsyncSession):
        pass

    async def get_all_by_revision_passing(
            self,
            session: AsyncSession,
            revision_passed: bool,
    ) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.revision.passed == revision_passed)
            .order_by(desc(Note.created_at))
        )
        return await self.__get_by_stmt(stmt, session=session)

    async def get_all_with_no_revisions(
            self,
            session: AsyncSession,
    ) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.revision is None)
            .order_by(desc(Note.created_at))
        )
        return await self.__get_by_stmt(stmt, session=session)

    async def get_all_by_user_with_any_revisions(
            self,
            session: AsyncSession,
            user_id: int
    ) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.revision is not None)
            .order_by(desc(Note.created_at))
        )
        return await self.__get_by_stmt(stmt, session=session)

    async def get_by_id(
            self,
            session: AsyncSession,
            note_id: int,
    ) -> Note | None:
        return await session.get(Note, note_id)
