from src.api.storage import BaseStorage
from .notes import NotesService
from .revision import RevisionService
from .token import TokenService
from .user import UserService


class Service:
    def __init__(
            self,
            storage: BaseStorage,
    ) -> None:
        token_service = TokenService(storage)
        self.__storage = storage
        self.__notes = NotesService(storage, token_service)
        self.__revision = RevisionService(storage)
        self.__user = UserService(storage, token_service)
        self.__token = token_service

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
