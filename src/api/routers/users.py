from fastapi import APIRouter, Depends, HTTPException, status

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


@router.get("/")
async def get_users(
        service: Service = Depends(get_service)
) -> GetManyUsersResponse:
    """return all users"""
    res = await service.user.get_all_users()
    return res


@router.get("/me")
async def get_me(
        service: Service = Depends(get_service),
) -> User:
    pass


@router.post("/register")
async def register_user(
        data: UserRegisterRequest,
        service: Service = Depends(get_service),
) -> UserAuthorizedResponse:
    pass


@router.post("/login")
async def login_user(
        data: UserLoginRequest,
        service: Service = Depends(get_service),
) -> UserAuthorizedResponse:
    pass


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        service: Service = Depends(get_service)
) -> User:
    """get user by provided id"""

    user = await service.user.get_by_id(user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User with id=%d not found" % user_id
    )
