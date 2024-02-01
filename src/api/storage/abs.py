from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import User, Note, Revision, Token


class BaseUserStorage(ABC):
    """BaseUserStorage is interface of storage which encapsulates all
    necessary logic of storing and getting and filtering users in it."""

    @abstractmethod
    async def create(
            self,
            user: User,
            *,
            session: AsyncSession,
    ) -> User:
        """Creates user and return created object back"""
        pass

    @abstractmethod
    async def get_user_by_id(
            self,
            user_id: int,
            *,
            session: AsyncSession,
    ) -> User | None:
        """
        get_user_by_id

        Returns user by provided id if it stored in and None object
        if not, respectively.
        """
        pass

    @abstractmethod
    async def get_users(self, *, session: AsyncSession) -> list[User]:
        """
        get_users

        Returns all stored users back.
        """
        pass

    @abstractmethod
    async def can_check(self, user_id: int, *, session: AsyncSession) -> bool:
        pass


class BaseNotesStorage(ABC):
    """BaseNotesStorage is interface of store, which provide all
    necessary methods to store, read and update Notes in system."""

    @abstractmethod
    async def create(self, note: Note, *, session: AsyncSession) -> Note:
        """create stores note to system"""
        pass

    @abstractmethod
    async def update(
            self,
            note: Note,
            *,
            session: AsyncSession,
            **kwargs
    ) -> None:
        """update updates note and returns changed Note to user"""
        pass

    @abstractmethod
    async def delete(self, note: Note, *, session: AsyncSession) -> None:
        """deletes note"""
        pass

    @abstractmethod
    async def get_all_by_user_id_with_status(
            self,
            user_id: int,
            status: int,
            session: AsyncSession,
    ) -> list[Note]:
        """
        return all notes, related to user with status.

        Statuses:
        -1 Not
        """
        pass

    @abstractmethod
    async def get_all_by_user_id(
            self,
            user_id: int,
            *,
            session: AsyncSession
    ) -> list[Note]:
        """return all notes, related to user with provided id"""
        pass


class BaseRevisionsStorage(ABC):
    """BaseRevisionsStorage is interface of store, which provide all
    necessary methods to store, read and update Revisions in system."""

    @abstractmethod
    async def create(
            self,
            revision: Revision,
            *,
            session: AsyncSession,
    ) -> Revision:
        pass

    @abstractmethod
    async def get_all_by_user(
            self,
            user_id: int,
            *,
            session: AsyncSession,
    ) -> list[Revision]:
        pass

    @abstractmethod
    async def get_all_by_note_id(
            self,
            note_id: int,
            *,
            session: AsyncSession,
    ) -> list[Revision]:
        pass

    @abstractmethod
    async def get_by_id(
            self,
            revision_id: int,
            *,
            session: AsyncSession,
    ) -> Revision | None:
        pass

    @abstractmethod
    async def get_all(self, *, session: AsyncSession) -> list[Revision]:
        pass


class BaseTokenStorage(ABC):
    @abstractmethod
    async def create(self, token: Token, *, session: AsyncSession) -> Token:
        pass

    @abstractmethod
    async def get_by_token_value(
            self,
            value: str,
            *,
            session: AsyncSession,
    ) -> Token | None:
        pass


class BaseStorage(ABC):
    @abstractmethod
    def user(self) -> BaseUserStorage:
        pass

    @abstractmethod
    def revision(self) -> BaseRevisionsStorage:
        pass

    @abstractmethod
    def note(self) -> BaseNotesStorage:
        pass

    @abstractmethod
    def token(self) -> BaseTokenStorage:
        pass
