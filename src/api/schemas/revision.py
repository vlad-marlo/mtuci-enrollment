from pydantic import BaseModel


class RevisionShortInfo(BaseModel):
    id: int
    text: str
    created_by: int
    passed: bool
