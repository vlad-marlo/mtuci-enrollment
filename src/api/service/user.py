import random
import string

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ServiceException
from src.api.schemas import (
    GetManyUsersResponse,
    User,
    UserRegisterRequest,
    UserLoginRequest,
    UserAuthorizedResponse,
)
from src.api.storage import BaseStorage
from src.core.models import Token
from src.core.models.user import User as DatabaseUser


class UserService:
    def __init__(self, storage: BaseStorage):
        self.__storage = storage

    async def get_all_users(
            self,
            session: AsyncSession,
    ) -> GetManyUsersResponse:
        users_from_db = await self.__storage.user().get_users(session=session)
        result = [User.model_validate(x).short_info() for x in users_from_db]
        response = GetManyUsersResponse(
            result=result,
            count=len(result),
        )
        return response

    async def get_by_id(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> User | None:
        user_from_db = await self.__storage.user().get_user_by_id(
            user_id,
            session=session,
        )
        return User.model_validate(user_from_db) if user_from_db else None

    async def register_user(
            self,
            user_data: UserRegisterRequest,
            session: AsyncSession,
    ) -> UserAuthorizedResponse | None:
        user_dict = user_data.model_dump()
        user_dict["password"] = user_data.password.get_secret_value()
        user = DatabaseUser(**user_dict)
        async with session.begin():
            user = await self.__storage.user().create(
                user,
                session=session,
            )
            token = self.__generate_token(user.id)
            token = await self.__storage.token().create(
                token,
                session=session,
            )
        return UserAuthorizedResponse(token=token.token)

    @staticmethod
    def __generate_token(user_id: int) -> Token:
        token = random.choices(string.printable, k=20)
        return Token(user_id=user_id, token=token)
