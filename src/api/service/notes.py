from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.notes import GetAllNotesResponse, NoteShortInfo
from src.api.schemas.revision import RevisionShortInfo
from src.api.storage import BaseStorage
from src.core.models import Note, Revision


class NotesService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage

    async def get_all(
            self,
            session: AsyncSession,
            created_by: int | None = None,
            revision_passed: str | None = None,
    ) -> GetAllNotesResponse:
        notes = await self.__get_all_with_no_user_id(
            session=session,
            revision_passed=revision_passed,
        ) if created_by is None else await self.__get_all_with_user_id(
            session=session,
            revision_passed=revision_passed,
            user_id=created_by,
        )
        GetAllNotesResponse(
            result=NoteShortInfo()
        )

    async def __get_short_info(
            self,
            session: AsyncSession,
            note: Note,
    ) -> NoteShortInfo:
        revision: Revision | None = await (
            self.__storage.revision().get_by_note_id(
                note.id,
                session=session,
            )
        )
        result = NoteShortInfo(
            id=note.id,
            created_at=note.created_at,
            created_by=note.created_by,
            text=note.text,
        )

        if revision is None:
            return result
        revision_short = RevisionShortInfo(
            id=revision.id,
            text=revision.text,
            passed=revision.passed,
            created_by=revision.created_by
        )
        return NoteShortInfo(
            id=note.id,
            revision=revision_short,
            created_by=note.created_by,
            created_at=note.created_at,
            text=note.text,
        )

    async def __get_all_with_user_id(
            self,
            session: AsyncSession,
            user_id: int,
            revision_passed: str | None = None,
    ) -> list[Note]:
        if revision_passed is None:
            return await self.__storage.note().get_all_by_user_id(
                user_id,
                session=session,
            )
        return self.__get_all_with_user_and_revision(
            session=session,
            user_id=user_id,
            revision_passed=revision_passed,
        )

    async def __get_all_with_no_user_id(
            self,
            session: AsyncSession,
            revision_passed: bool | None = None,
    ) -> list[Note]:
        if revision_passed is None:
            return await self.__storage.note().get_all(session)
        return await self.__get_all_with_no_user_and_revision(
            session=session,
            revision_passed=revision_passed,
        )

    async def __get_all_with_no_user_and_revision(
            self,
            session: AsyncSession,
            revision_passed: bool | None = None,
    ) -> list[Note]:
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
