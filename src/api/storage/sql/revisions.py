from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from src.api.storage import BaseRevisionsStorage
from src.core.models import Revision
from src.sync_decorator import with_lock

lock = with_lock()


class RevisionStorage(BaseRevisionsStorage):
    def __init__(self, session: AsyncSession):
        self.__session = session

    def replace_session(self, session: AsyncSession) -> None:
        self.__session = session

    @lock
    async def create(self, revision: Revision) -> Revision:
        self.__session.add(revision)
        await self.__session.commit()
        return revision

    @lock
    async def get_all_by_user(self, user_id: int) -> list[Revision]:
        stmt = select(Revision).where(Revision.created_by == user_id)
        result = await self.__session.execute(stmt)
        revisions = result.scalars().all()
        return list(revisions)

    @lock
    async def get_all_by_note_id(self, note_id: int) -> Revision | None:
        stmt = select(Revision).where(Revision.note_id == note_id)
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    @lock
    async def get_by_id(self, revision_id: int) -> Revision | None:
        stmt = select(Revision).where(Revision.id == revision_id)
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    @lock
    async def get_all(self) -> list[Revision]:
        stmt = select(Revision).order_by(desc(Revision.created_at))
        result = await self.__session.execute(stmt)
        return result.scalars().all()
