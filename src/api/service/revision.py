from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ServiceException
from src.api.schemas.revision import RevisionCreateRequest, RevisionShortInfo
from src.api.service.token import TokenService
from src.api.storage import BaseStorage
from src.core.models import Revision


class RevisionService:
    def __init__(self, storage: BaseStorage, tokens: TokenService):
        self.__token = tokens
        self.__storage = storage

    async def create(
            self,
            note_id: int,
            revision: RevisionCreateRequest,
            token: str,
            session: AsyncSession,
    ) -> RevisionShortInfo:
        user_id = await self.__token.get_user_id(token, session)
        if user_id is None:
            raise ServiceException(
                detail="Unauthorized",
                code=status.HTTP_401_UNAUTHORIZED,
            )
        can_check = await self.__storage.user().can_check(
            user_id,
            session=session,
        )
        if not can_check:
            raise ServiceException(
                detail="no permission",
                code=status.HTTP_403_FORBIDDEN,
            )
        try:
            res = await self.__storage.revision().create(
                Revision(
                    text=revision.text,
                    note_id=note_id,
                    passed=revision.passed,
                    created_by=user_id,
                ),
                session=session
            )
        except Exception as e:
            raise ServiceException(
                detail="already exists",
                code=status.HTTP_409_CONFLICT,
                log=str(e)
            )
        return RevisionShortInfo(
            created_by=user_id,
            passed=revision.passed,
            id=res.id,
            text=revision.text,
        )

