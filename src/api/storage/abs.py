from abc import ABC, abstractmethod

from src.core.models import User, Note, Revision


class BaseUserStorage(ABC):
    """BaseUserStorage is interface of storage which encapsulates all
    necessary logic of storing and getting and filtering users in it."""

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """Creates user and return created object back"""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        get_user_by_id

        Returns user by provided id if it stored in and None object
        if not, respectively.
        """
        pass

    @abstractmethod
    async def get_users(self) -> list[User]:
        """
        get_users

        Returns all stored users back.
        """
        pass


class BaseNotesStorage(ABC):
    """BaseNotesStorage is interface of store, which provide all
    necessary methods to store, read and update Notes in system."""

    @abstractmethod
    async def create(self, note: Note) -> Note:
        """create stores note to system"""
        pass

    @abstractmethod
    async def update(self, note: Note) -> None:
        """update updates note and returns changed Note to user"""
        pass

    @abstractmethod
    async def delete(self, note: Note) -> None:
        """deletes note"""
        pass

    @abstractmethod
    async def get_all_by_user_id_with_status(
            self,
            user_id: int,
            status: int,
    ) -> list[Note]:
        """
        return all notes, related to user with status.

        Statuses:
        -1 Not
        """
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[Note]:
        """return all notes, related to user with provided id"""
        pass


class BaseRevisionsStorage(ABC):
    """BaseRevisionsStorage is interface of store, which provide all
    necessary methods to store, read and update Revisions in system."""

    @abstractmethod
    async def create(self, revision: Revision) -> Revision:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: int) -> list[Revision]:
        pass

    @abstractmethod
    async def get_all_by_note_id(self, note_id: int) -> list[Revision]:
        pass

    @abstractmethod
    async def get_by_id(self, revision_id: int) -> Revision | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Revision]:
        pass
