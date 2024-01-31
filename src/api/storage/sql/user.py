from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseUserStorage
from src.core.models import User


class UserStorage(BaseUserStorage):
    def __init__(self, session: AsyncSession):
        self.__session = session

    def replace_session(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, user: User) -> User:
        self.__session.add(user)
        await self.__session.commit()
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.__session.get(User, user_id)

    async def get_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await self.__session.execute(stmt)
        users: list[User] = [u for u in result.scalars().all()]
        return users

    async def can_check(self, user_id: int) -> bool:
        stmt = select(User.can_check).where(User.id == user_id)
        res = await self.__session.execute(stmt)
        res.scalar_one_or_none()
        return bool(res)
