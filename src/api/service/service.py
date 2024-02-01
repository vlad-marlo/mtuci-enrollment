from .notes import NotesService
from .revision import RevisionService
from .token import TokenService
from .user import UserService

from src.api.storage import BaseStorage


class Service:
    def __init__(
            self,
            storage: BaseStorage,
    ) -> None:
        self.__storage = storage
        self.__notes = NotesService(storage)
        self.__revision = RevisionService(storage)
        self.__token = TokenService(storage)
        self.__user = UserService(storage, self.__token)

    @property
    def notes(self) -> NotesService:
        return self.__notes

    @property
    def revision(self) -> RevisionService:
        return self.__revision

    @property
    def user(self) -> UserService:
        return self.__user

    @property
    def token(self) -> TokenService:
        return self.__token