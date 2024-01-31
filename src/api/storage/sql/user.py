from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseUserStorage
from src.core.models import User
from src.sync_decorator import with_lock

lock = with_lock()


class UserStorage(BaseUserStorage):
    def __init__(self, session: AsyncSession):
        self.__session = session

    def replace_session(self, session: AsyncSession) -> None:
        self.__session = session

    @lock
    async def create(self, user: User) -> User:
        self.__session.add(user)
        await self.__session.commit()
        return user

    @lock
    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.__session.get(User, user_id)

    @lock
    async def get_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await self.__session.execute(stmt)
        users = result.scalars().all()
        return list(users)
