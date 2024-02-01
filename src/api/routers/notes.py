from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.notes import (
    GetAllNotesResponse,
    NoteCreationRequest,
    NoteUpdateRequest,
    NoteCreateResponse,
    Note,
)
from src.core.models import db_helper
from structlog import get_logger
from .service_helper import service
from ..exceptions import ServiceException

logger = get_logger()

router = APIRouter(
    tags=[
        "Notes",
    ],
    prefix="/notes"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
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
    try:
        resp = await service.notes.get_by_id(note_id, session)
    except ServiceException as e:
        raise HTTPException(detail=e.detail, status_code=e.code)
    except Exception as e:
        logger.error(f"got unexpected exception trowed {e}")
        raise HTTPException(
            detail="unknown error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        return resp


@router.patch("/{note_id}")
async def update_patch(
        note_id: int,
        token: str,
        req: NoteUpdateRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Note:
    return await update_logic(note_id, token, req, session)


@router.put("/{note_id}")
async def update_put(
        note_id: int,
        token: str,
        req: NoteUpdateRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Note:
    return await update_logic(note_id, token, req, session)


async def update_logic(
        note_id: int,
        token: str,
        req: NoteUpdateRequest,
        session: AsyncSession,
) -> Note:
    return await service.notes.update(
        note_id=note_id,
        token=token,
        text=req.text,
        session=session,
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        note_id: int,
        token: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    try:
        await service.notes.delete(note_id, token, session)
    except ServiceException as e:
        raise HTTPException(detail=e.detail, status_code=e.code)
    except Exception as e:
        logger.error(f"got unexpected trowed exception e={e}")
        raise HTTPException(
            detail="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
