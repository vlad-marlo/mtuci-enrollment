from src.api.storage import BaseUserStorage
from src.api.schemas import (
    GetManyUsersResponse,
    User,
)


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


