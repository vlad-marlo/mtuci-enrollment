from pydantic import BaseModel
from .user import UserShortInfo


class RevisionShortInfo(BaseModel):
    id: int
    text: str
    created_by: UserShortInfo
    passed: bool
