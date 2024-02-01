from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.notes import GetAllNotesResponse, NoteShortInfo
from src.api.storage import BaseStorage
from src.core.models import Note


class NotesService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage

    async def get_all(
            self,
            session: AsyncSession,
            created_by: int | None = None,
            revision_passed: str | None = None,
            has_revision: bool | None = None,
    ) -> GetAllNotesResponse:
        notes = await self.__get_all_with_no_user_id(
            session=session,
            revision_passed=revision_passed,
            has_revision=has_revision,
        ) if created_by is None else await self.__get_all_with_user_id(
            session=session,
            revision_passed=revision_passed,
            has_revision=has_revision,
            user_id=created_by,
        )
        GetAllNotesResponse(
            result=NoteShortInfo()
        )

    async def __get_all_with_user_id(
            self,
            session: AsyncSession,
            user_id: int,
            revision_passed: str | None = None,
            has_revision: bool | None = None,
    ) -> list[Note]:
        if has_revision is None:
            return await self.__storage.note().get_all_by_user_id(
                user_id,
                session=session,
            )
        if has_revision:
            return self.__get_all_with_user_and_revision(
                session=session,
                user_id=user_id,
                revision_passed=revision_passed,
            )
        return await self.__storage.note().get_all_with_user_and_no_revisions(
            session
        )

    async def __get_all_with_no_user_id(
            self,
            session: AsyncSession,
            revision_passed: bool | None = None,
            has_revision: bool | None = None,
    ) -> list[Note]:
        if has_revision is None:
            return await self.__storage.note().get_all(session)
        if has_revision:
            return self.__get_all_with_no_user_and_revision(
                session=session,
                revision_passed=revision_passed,
            )
        return await self.__storage.note().get_all_with_no_revisions(session)

    async def __get_all_with_no_user_and_revision(
            self,
            session: AsyncSession,
            revision_passed: bool | None = None,
    ) -> list[Note]:
        if revision_passed is None:
            return await self.__storage.note().get_all_with_revisions(session)
        return await self.__storage.note().get_all_by_revision_passing(
            session,
            revision_passed,
        )

    async def __get_all_with_user_and_revision(
            self,
            session: AsyncSession,
            user_id: int,
            revision_passed: None | bool,
    ) -> list[Note]:
        if revision_passed is None:
            return await (
                self.__storage.note().
                get_all_by_user_with_any_revisions(
                    session=session,
                    user_id=user_id,
                )
            )
        return await self.__storage.note().get_all_by_user_id_and_passing(
            session=session,
            user_id=user_id,
            passed=revision_passed
        )
