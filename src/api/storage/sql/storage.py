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
