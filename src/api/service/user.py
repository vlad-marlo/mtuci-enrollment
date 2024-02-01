import random
import string

from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ServiceException
from src.api.schemas import (
    GetManyUsersResponse,
    User,
    UserRegisterRequest,
    UserLoginRequest,
    UserAuthorizedResponse,
)
from src.api.service.token import TokenService
from src.api.storage import BaseStorage
from src.core.models import Token
from src.core.models.user import User as DatabaseUser
from src.logger import logger


class UserService:
    def __init__(self, storage: BaseStorage, tokens: TokenService):
        self.__tokens = tokens
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

    async def get_by_phone(
            self,
            phone: str,
            session: AsyncSession,
    ) -> User | None:
        user_from_db = await self.__storage.user().get_by_phone(
            phone,
            session=session,
        )
        return User.model_validate(user_from_db) if user_from_db else None

    async def register_user(
            self,
            user_data: UserRegisterRequest,
            session: AsyncSession,
    ) -> UserAuthorizedResponse | None:
        user_dict = user_data.model_dump()
        logger.info(f"user_dict={user_dict}")
        user = DatabaseUser(**user_dict)
        logger.info(f"user={user}")

        try:

            user = await self.__storage.user().create(
                user,
                session=session,
            )
            token = self.__generate_token(user.id)
            token = await self.__storage.token().create(
                token,
                session=session,
            )
        except Exception as e:
            raise ServiceException(log=e, detail="Internal error")
        else:
            return UserAuthorizedResponse(token=token.token)

    @staticmethod
    def __generate_token(user_id: int) -> Token:
        token = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=20,
            ),
        )
        return Token(user_id=user_id, token=token)

    async def login(
            self,
            user: UserLoginRequest,
            session: AsyncSession,
    ) -> UserAuthorizedResponse:
        auth_user = await self.__storage.user().get_auth_data_by_phone(
            phone=user.phone,
            session=session,
        )
        if auth_user is None or auth_user.password != user.password:
            raise ServiceException(
                code=status.HTTP_401_UNAUTHORIZED,
                detail="Bad auth credentials",
            )
        try:
            token = await (
                self.__storage
                .token()
                .create(
                    self.__generate_token(auth_user.id),
                    session=session,
                )
            )
            self.__tokens.add_token(token)
        except Exception as e:
            raise ServiceException(log=f"unknown exception {e}")
        return UserAuthorizedResponse(token=token.token)

    async def get_by_token(self, token: str, session: AsyncSession) -> User:
        unauthorized = ServiceException(
            detail="unauthorized",
            code=status.HTTP_401_UNAUTHORIZED
        )

        user_id: int | None = await self.__tokens.get_user_id(token, session)
        if user_id is None:
            raise unauthorized
        try:
            user = await self.__storage.user().get_user_by_id(
                user_id,
                session=session,
            )
            if user is None:
                raise unauthorized
        except ServiceException as e:
            raise HTTPException(detail=e.detail, status_code=e.code)
        except Exception as e:
            logger.error(f"got unexpected exception {e=}")
            raise HTTPException(
                detail="unknown error",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            return user
