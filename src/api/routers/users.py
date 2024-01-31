from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
from .service_helper import get_service

s = Service(Storage(db_helper.get_scoped_session()))

router = APIRouter(
    tags=[
        "Users",
    ],
    prefix="/users"
)


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> User:
    service = get_service(session)

    res = await service.user.get_by_id(user_id)
    return res


@router.get("/")
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> GetManyUsersResponse:
    service = get_service(session)
    return service.user.get_all_users()


@router.get("/me")
async def get_me() -> User:
    pass


@router.post("/register")
async def register_user(data: UserRegisterRequest) -> UserAuthorizedResponse:
    pass


@router.post("/login")
async def login_user(data: UserLoginRequest) -> UserAuthorizedResponse:
    pass
