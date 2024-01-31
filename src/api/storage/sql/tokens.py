from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api.storage import BaseTokenStorage
from src.core.models import Token


class TokenStorage(BaseTokenStorage):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create(self, token: Token) -> Token:
        self.__session.add(token)
        await self.__session.commit()
        return token

    async def get_by_token_value(self, value: str) -> Token | None:
        stmt = select(Token).where(Token.token == value)
        res = await self.__session.execute(stmt)
        return res.scalar_one_or_none()
