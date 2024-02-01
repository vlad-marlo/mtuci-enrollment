from datetime import datetime

from pydantic import BaseModel

from src.api.schemas.revision import RevisionShortInfo


class NoteCreationRequest(BaseModel):
    text: str


class NoteCreateResponse(BaseModel):
    id: int
    text: str


class NoteUpdateRequest(BaseModel):
    text: str


class Note(BaseModel):
    id: int
    text: str
    created_at: datetime
    created_by: int
    revision: RevisionShortInfo | None = None


class GetAllNotesResponse(BaseModel):
    result: list[Note]
