from datetime import datetime

from pydantic import BaseModel

from src.api.schemas.revision import RevisionShortInfo


class Note(BaseModel):
    id: int
    text: str
    created_at: datetime


class NoteCreationRequest(BaseModel):
    text: str


class NoteUpdateRequest(BaseModel):
    text: str


class NoteShortInfo(BaseModel):
    id: int
    text: str
    created_at: datetime
    created_by: int
    revision: RevisionShortInfo | None = None


class GetAllNotesResponse(BaseModel):
    result: list[NoteShortInfo]