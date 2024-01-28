from abc import ABC, abstractmethod

from src.core.models import User


class BaseUserStorage(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def get_users(self) -> list[User]:
        pass
