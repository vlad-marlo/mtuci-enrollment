from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
