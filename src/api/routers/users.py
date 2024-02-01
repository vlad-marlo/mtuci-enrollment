from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ServiceException
from src.api.schemas import (
    GetManyUsersResponse,
    User,
    UserRegisterRequest,
    UserLoginRequest,
    UserAuthorizedResponse,
)
from src.api.service import Service
from src.api.storage.sql import Storage
from src.core.models import db_helper

__service = Service(Storage())

router = APIRouter(
    tags=[
        "Users",
    ],
    prefix="/users"
)


@router.get("/")
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> GetManyUsersResponse:
    """return all users"""
    res = await __service.user.get_all_users(session)
    return res


@router.get("/me")
async def get_me(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    pass


@router.post("/register")
async def register_user(
        data: UserRegisterRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserAuthorizedResponse:
    pass


@router.post("/login")
async def login_user(
        data: UserLoginRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserAuthorizedResponse:
    pass


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> User:
    """get user by provided id"""

    user = await service.user.get_by_id(user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User with id=%d not found" % user_id
    )
