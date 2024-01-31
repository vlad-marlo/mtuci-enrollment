from src.api.schemas import (
    GetManyUsersResponse,
    User,
)
from src.api.storage import BaseUserStorage


class UserService:
    def __init__(self, storage: BaseUserStorage):
        self.__storage = storage

    async def get_all_users(self) -> GetManyUsersResponse:
        users_from_db = await self.__storage.get_users()
        result = [User.model_validate(x).short_info() for x in users_from_db]
        response = GetManyUsersResponse(
            result=result,
            count=len(result),
        )
        return response

    async def get_by_id(self, user_id: int) -> User:
        user_from_db = await self.__storage.get_user_by_id(user_id)
        return User.model_validate(user_from_db)

