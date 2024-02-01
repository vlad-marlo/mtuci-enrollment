from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseStorage
from src.core.models import Token
from src.logger import logger


class TokenService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage
        self.__synced: bool = False
        self.__tokens: dict[str, int] = dict()

    async def sync_all_tokens(self, session: AsyncSession) -> None:
        tokens: list[Token] = await self.__storage.token().get_all(
            session=session,
        )
        logger.error(f"type={type(tokens)} tokens={tokens}")

        for token in tokens:
            self.__tokens[token.token] = token.user_id
            logger.error(str(token))
        self.__synced = True

    async def get_user_id(
            self,
            token: str,
            session: AsyncSession,
    ) -> int | None:
        if not self.__synced:
            await self.sync_all_tokens(session)
            logger.error(token)
        if token not in self.__tokens.keys():
            return None
        return self.__tokens[token]

    def add_token(self, token: Token):
        if token is None:
            return
        self.__tokens[token.token] = token.user_id
