from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import (
    BaseNotesStorage,
    BaseRevisionsStorage,
    BaseStorage,
    BaseUserStorage,
)
from src.api.storage.sql import (
    NotesStorage,
    RevisionStorage,
    UserStorage,
)
from src.core.models import db_helper


class Storage(BaseStorage):
    def __init__(self, session: AsyncSession):
        self.__notes = NotesStorage(session)
        self.__revision = RevisionStorage(session)
        self.__user = UserStorage(session)

    def note(self) -> BaseNotesStorage:
        return self.__notes

    def revision(self) -> BaseRevisionsStorage:
        return self.__revision

    def user(self) -> BaseUserStorage:
        return self.__user

    def replace_session(self, session: AsyncSession) -> None:
        self.__notes.replace_session(session)
        self.__revision.replace_session(session)
        self.__user.replace_session(session)


__storage = Storage(db_helper.get_scoped_session())


def get_storage(session: AsyncSession) -> Storage:
    __storage.replace_session(session)
    return __storage
