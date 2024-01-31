from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, SecretStr, ConfigDict


class UserShortInfo(BaseModel):
    id: int
    full_name: str
    position: str
    can_check: bool


class User(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

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
            position=self.position,
            can_check=self.can_check,
            full_name=f"{self.first_name} {self.middle_name} {self.last_name}",
        )


class GetManyUsersResponse(BaseModel):
    count: int
    result: list[UserShortInfo]


class UserRegisterRequest(BaseModel):
    phone: Annotated[str, MinLen(11), MaxLen(12)]
    password: SecretStr
    first_name: str
    middle_name: str
    last_name: str
    position: str
    can_check: bool = False


class UserAuthorizedResponse(BaseModel):
    token: str


class UserLoginRequest(BaseModel):
    phone: str
    password: str
