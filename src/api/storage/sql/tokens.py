from sqlalchemy import select, Result, insert
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from src.api.storage import BaseTokenStorage
from src.core.models import Token


class TokenStorage(BaseTokenStorage):
    def __init__(self):
        return

    async def create(self, token: Token, *, session: AsyncSession) -> Token:
        session.add(token)
        await session.commit()
        return token

    async def get_by_token_value(
            self,
            value: str,
            *,
            session: AsyncSession,
    ) -> Token | None:
        stmt = select(Token).where(Token.token == value)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, *, session: AsyncSession) -> list[Token]:
        stmt = select(Token).order_by(Token.id)
        result: Result = await session.execute(stmt)

        return [t for t in result.scalars().all()]
