from .notes import NotesService
from .revision import RevisionService
from .user import UserService

from src.api.storage import BaseStorage


class Service:
    def __init__(
            self,
            storage: BaseStorage,
    ) -> None:
        self.__storage = storage
        self.__notes = NotesService(storage.note())
        self.__revision = RevisionService(storage.revision())
        self.__user = UserService(storage.user())

    @property
    def notes(self) -> NotesService:
        return self.__notes

    @property
    def revision(self) -> RevisionService:
        return self.__revision

    @property
    def user(self) -> UserService:
        return self.__user
