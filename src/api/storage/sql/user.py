from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.storage import BaseUserStorage
from src.core.models import User


class UserStorage(BaseUserStorage):
    def __init__(self) -> None:
        return

    async def create(
            self,
            user: User,
            *,
            session: AsyncSession,
    ) -> User:
        session.add(user)
        await session.commit()
        return user

    async def get_user_by_id(
            self,
            user_id: int,
            *,
            session: AsyncSession,
    ) -> User | None:
        return await session.get(User, user_id)

    async def get_by_phone(
            self,
            phone: str,
            *,
            session: AsyncSession,
    ) -> User | None:
        stmt = select(User).where(User.phone == phone)
        res = await session.scalars(stmt)
        return res.one_or_none()

    async def get_users(
            self,
            *,
            session: AsyncSession,
    ) -> list[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await session.execute(stmt)
        users: list[User] = [u for u in result.scalars().all()]
        return users

    async def get_auth_data_by_phone(
            self,
            phone: str,
            *,
            session: AsyncSession,
    ) -> User | None:
        stmt = (
            select(User.id, User.password).
            where(User.phone == phone)
        )
        scalar = await session.scalars(stmt)
        res = scalar.one_or_none()
        if res:
            return User(id=res.id, password=res.password, phone=phone)
        return

    async def can_check(
            self,
            user_id: int,
            *,
            session: AsyncSession,
    ) -> bool:
        stmt = select(User.can_check).where(User.id == user_id)
        res = await session.execute(stmt)
        res.scalar_one_or_none()
        return bool(res)
