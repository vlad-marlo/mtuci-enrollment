from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.notes import (
    GetAllNotesResponse,
    NoteCreationRequest,
    NoteCreateResponse,
    Note,
)
from src.core.models import db_helper
from src.logger import logger
from .service_helper import service
from ..exceptions import ServiceException

router = APIRouter(
    tags=[
        "Users",
    ],
    prefix="/notes"
)


@router.post("/")
async def create(
        token: str,
        request: NoteCreationRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> NoteCreateResponse:
    try:
        response = await service.notes.create(token, request.text, session)
    except ServiceException as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    else:
        return response


@router.get("/")
async def get_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        created_by: int | None = None,
        revision_passed: bool | None = None,
) -> GetAllNotesResponse:
    """
    Get users.
    If phone is provided and user exists in database, then it will be returned
    back. If not exists or phone not provided
    """
    try:
        response = await service.notes.get_all(
            session,
            created_by=created_by,
            revision_passed=revision_passed,
        )
    except ServiceException as e:
        raise HTTPException(detail=e.detail, status_code=e.code)
    else:
        return response


@router.get("/{note_id}")
async def get_by_id(
        note_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Note:
    service.notes.get_by_id()

