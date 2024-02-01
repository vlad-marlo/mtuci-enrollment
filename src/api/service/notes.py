from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ServiceException
from src.api.schemas.notes import (
    GetAllNotesResponse,
    Note,
    NoteCreateResponse,
)
from src.api.schemas.revision import RevisionShortInfo
from src.api.service.token import TokenService
from src.api.storage import BaseStorage
from src.core.models import Note as DBNote, Revision


class NotesService:
    def __init__(self, storage: BaseStorage, token: TokenService):
        self.__token = token
        self.__storage = storage

    async def get_all(
            self,
            session: AsyncSession,
            created_by: int | None = None,
            revision_passed: bool | None = None,
    ) -> GetAllNotesResponse:
        notes = await self.__get_all_with_no_user_id(
            session=session,
            revision_passed=revision_passed,
        ) if created_by is None else await self.__get_all_with_user_id(
            session=session,
            revision_passed=revision_passed,
            user_id=created_by,
        )
        res = []
        for note in notes:
            info = await self.__get_full_info(session, note)
            res.append(info)
        return GetAllNotesResponse(
            result=res
        )

    async def __get_full_info(
            self,
            session: AsyncSession,
            note: DBNote,
    ) -> Note:
        revision: Revision | None = await (
            self.__storage.revision().get_by_note_id(
                note.id,
                session=session,
            )
        )
        result = Note(
            id=note.id,
            created_at=note.created_at,
            created_by=note.created_by,
            text=note.text,
            revision=None
        )

        if revision is None:
            return result
        revision_short = RevisionShortInfo(
            id=revision.id,
            text=revision.text,
            passed=revision.passed,
            created_by=revision.created_by
        )
        result.revision = revision_short
        return result

    async def __get_all_with_user_id(
            self,
            session: AsyncSession,
            user_id: int,
            revision_passed: str | None = None,
    ) -> list[DBNote]:
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
    ) -> list[DBNote]:
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
    ) -> list[DBNote]:
        return await self.__storage.note().get_all_by_revision_passing(
            session,
            revision_passed,
        )

    async def __get_all_with_user_and_revision(
            self,
            session: AsyncSession,
            user_id: int,
            revision_passed: None | bool,
    ) -> list[DBNote]:
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

    async def create(
            self,
            user_token: str,
            text: str,
            session: AsyncSession,
    ) -> NoteCreateResponse:
        user_id = await self.__token.get_user_id(user_token, session=session)
        if user_id is None:
            raise ServiceException(
                detail="unauthorized",
                code=status.HTTP_401_UNAUTHORIZED,
            )
        note = DBNote(
            text=text,
            is_deleted=False,
            created_by=user_id,
        )
        try:
            note = await self.__storage.note().create(note, session=session)
        except Exception as e:
            raise ServiceException(
                detail="unknown error",
                log=f"exception e={e}",
            )
        else:
            return NoteCreateResponse(
                id=note.id,
                text=note.text,
            )

    async def get_by_id(self, note_id: int, session: AsyncSession) -> Note:
        note = await self.__storage.note().get_by_id(session, note_id)
        if note is None:
            raise ServiceException(
                detail="not found",
                code=status.HTTP_404_NOT_FOUND,
            )
        return await self.__get_full_info(session, note)

    async def update(
            self,
            note_id: int,
            token: str,
            text: str,
            session: AsyncSession,
    ) -> Note:
        user = self.__token.get_user_id(token, session)
        if user is None:
            raise ServiceException(
                code=status.HTTP_401_UNAUTHORIZED,
                detail="bad auth credentials"
            )
        if not self.__storage.note().user_can_edit(note_id, user, session):
            raise ServiceException(
                code=status.HTTP_403_FORBIDDEN,
                detail="you are not a creator of this note"
            )
        await self.__storage.note().update(
            note_id=note_id,
            text=text,
            session=session,
        )
        return await self.get_by_id(note_id, session)

    async def delete(
            self,
            note_id: int,
            token: str,
            session: AsyncSession,
    ) -> None:
        user = self.__token.get_user_id(token, session)
        if user is None:
            raise ServiceException(
                code=status.HTTP_401_UNAUTHORIZED,
                detail="bad auth credentials"
            )
        if not self.__storage.note().user_can_edit(note_id, user, session):
            raise ServiceException(
                code=status.HTTP_403_FORBIDDEN,
                detail="you are not a creator of this note"
            )
        await self.__storage.note().delete(note_id, session=session)
