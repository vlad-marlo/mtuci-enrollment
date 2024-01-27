from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import UserRegisterRequest
from src.core.models import User
from src.sync_decorator import with_lock

decorator = with_lock()


class UserStorage:
    def __init__(self, session: AsyncSession):
        self._session = session

    @decorator
    async def create_user(self, user: UserRegisterRequest) -> User:
        user = User(**user.model_dump())
        self._session.add(user)
        await self._session.commit()
        return user

    @decorator
    async def get_user_by_id(self, user_id: int) -> User:
        return await self._session.get(User, user_id)

    @decorator
    async def get_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await self._session.execute(stmt)
        users = result.scalars().all()
        return list(users)
