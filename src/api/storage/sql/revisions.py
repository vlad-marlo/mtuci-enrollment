from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseRevisionsStorage
from src.core.models import Revision


class RevisionStorage(BaseRevisionsStorage):
    def __init__(self):
        return

    async def create(
            self,
            revision: Revision,
            *,
            session: AsyncSession,
    ) -> Revision:
        session.add(revision)
        await session.commit()
        return revision

    async def get_all_by_user(
            self,
            user_id: int,
            *,
            session: AsyncSession,
    ) -> list[Revision]:
        stmt = select(Revision).where(Revision.created_by == user_id)
        result = await session.execute(stmt)
        revisions = result.scalars().all()
        return list(revisions)

    async def get_by_note_id(
            self,
            note_id: int,
            *,
            session: AsyncSession,
    ) -> Revision | None:
        stmt = select(Revision).where(Revision.note_id == note_id)
        result = await session.execute(stmt)
        return result.scalar()

    async def get_by_id(
            self,
            revision_id: int,
            *,
            session: AsyncSession,
    ) -> Revision | None:
        stmt = select(Revision).where(Revision.id == revision_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
            self,
            *,
            session: AsyncSession,
    ) -> list[Revision]:
        stmt = select(Revision).order_by(desc(Revision.created_at))
        result = await session.execute(stmt)
        return result.scalars().all()
