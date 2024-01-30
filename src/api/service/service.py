from .notes import NotesService
from .revision import RevisionService
from .user import UserService


class Service:
    def __init__(
            self,
            *,
            notes_service: NotesService,
            revision_service: RevisionService,
            user_service: UserService,
    ) -> None:
        self.__notes = notes_service
        self.__revision = revision_service
        self.__user = user_service

    @property
    def notes(self) -> NotesService:
        return self.__notes

    @property
    def revision(self) -> RevisionService:
        return self.__revision

    @property
    def user(self) -> UserService:
        return self.__user
