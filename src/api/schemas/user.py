from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, SecretStr


class UserShortInfo(BaseModel):
    id: int
    phone: str
    full_name: str


class User(BaseModel):
    id: int
    phone: Annotated[str, MinLen(11), MaxLen(12)]
    first_name: str
    middle_name: str
    last_name: str
    position: str
    can_check: bool

    def short_info(self) -> UserShortInfo:
        return UserShortInfo(
            id=self.id,
            phone=self.phone,
            full_name=f"{self.first_name} {self.middle_name} {self.last_name}",
        )


class GetManyUsersResponse(BaseModel):
    count: int
    result: list[User]


class UserRegisterRequest(BaseModel):
    phone: Annotated[str, MinLen(11), MaxLen(12)]
    password: SecretStr
    first_name: str
    middle_name: str
    last_name: str
    position: str
    can_check: bool = False


class UserAuthorizedResponse(BaseModel):
    pass


class UserLoginRequest(BaseModel):
    phone: str
    password: str
