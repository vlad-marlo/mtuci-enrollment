from fastapi import APIRouter

router: APIRouter = APIRouter(
    tags=(
        "Users",
    ),
    prefix="/users"
)