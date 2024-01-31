from src.api.storage import (
    BaseNotesStorage,
    BaseRevisionsStorage,
    BaseStorage,
    BaseTokenStorage,
    BaseUserStorage,
)
from src.api.storage.sql.notes import NotesStorage
from src.api.storage.sql.revisions import RevisionStorage
from src.api.storage.sql.tokens import TokenStorage
from src.api.storage.sql.user import UserStorage


class Storage(BaseStorage):
    def __init__(self):
        self.__notes = NotesStorage()
        self.__revision = RevisionStorage()
        self.__user = UserStorage()
        self.__token = TokenStorage()

    def note(self) -> BaseNotesStorage:
        return self.__notes

    def revision(self) -> BaseRevisionsStorage:
        return self.__revision

    def token(self) -> BaseTokenStorage:
        return self.__token

    def user(self) -> BaseUserStorage:
        return self.__user
