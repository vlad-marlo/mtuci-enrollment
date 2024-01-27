from fastapi import APIRouter
from src.api.schemas import (
    GetManyUsersResponse,
    User,
    UserRegisterRequest,
    UserLoginRequest,
    UserAuthorizedResponse,
)

router = APIRouter(
    tags=[
        "Users",
    ],
    prefix="/users"
)


@router.get("/{user_id}")
async def get_user_by_id(user_id: str) -> User:
    return User(id=int(user_id))


@router.get("/")
async def get_users() -> GetManyUsersResponse:
    pass


@router.get("/me")
async def get_me() -> User:
    pass


@router.post("/register")
async def register_user(data: UserRegisterRequest) -> UserAuthorizedResponse:
    pass


@router.post("/login")
async def login_user(data: UserLoginRequest) -> UserAuthorizedResponse:
    pass
