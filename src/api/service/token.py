from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseStorage
from src.core.models import Token


class TokenService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage
        self.__synced: bool = False
        self.__tokens: dict[str, int] = []

    async def sync_all_tokens(self, session: AsyncSession) -> None:
        tokens = await self.__storage.token().get_all(session=session)
        for token in tokens:
            self.__tokens[token.token] = token.user_id

    async def get_user_id(
            self,
            token: str,
            session: AsyncSession,
    ) -> int | None:
        if not self.__synced:
            await self.sync_all_tokens(session)
        return self.__tokens.get(token, None)

    def add_token(self, token: Token):
        if token is None:
            return
        self.__tokens[token.token] = token.user_id
