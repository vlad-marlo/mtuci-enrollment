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
from src.core.models import db_helper
from .service_helper import service

router = APIRouter(
    tags=[
        "Users",
    ],
    prefix="/users"
)


@router.get("/")
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        phone: str | None = None,
) -> GetManyUsersResponse:
    """
    Get users.
    If phone is provided and user exists in database, then it will be returned
    back. If not exists or phone not provided
    """
    if phone is not None:
        res = await service.user.get_by_id(phone, session=session)
        if res is not None:
            return User.model_validate(res)
    res = await service.user.get_all_users(session)
    return res


@router.get("/me")
async def get_me(
        token: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    try:
        user: User | None = await service.user.get_by_token(
            token,
            session=session,
        )
    except ServiceException as e:
        raise HTTPException(detail=e.detail, status_code=e.code)
    else:
        if user is None:
            raise HTTPException(
                detail="user not found",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return user


@router.post("/register")
async def register_user(
        data: UserRegisterRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserAuthorizedResponse:
    try:
        result = await service.user.register_user(data, session=session)
        if result is None:
            raise HTTPException(status_code=400, detail="something went wrong")
    except ServiceException as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    return result


@router.post("/login")
async def login_user(
        data: UserLoginRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserAuthorizedResponse:
    try:
        result = await service.user.login(data, session=session)
    except ServiceException as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    return result


@router.get("/{user_id}")
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> User:
    """get user by provided id"""

    user = await service.user.get_by_id(user_id, session=session)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User with id=%d not found" % user_id
    )
