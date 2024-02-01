from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import ServiceException
from src.api.schemas.revision import (
    RevisionCreateRequest,
    RevisionShortInfo
)
from src.core.models import db_helper
from src.logger import logger
from .service_helper import service

router = APIRouter(
    tags=[
        "Revisions",
    ],
)


@router.post("/notes/{note_id}/revision")
async def create_revision(
        note_id: int,
        token: str,
        revision: RevisionCreateRequest,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> RevisionShortInfo:
    """
    Get users.
    If phone is provided and user exists in database, then it will be returned
    back. If not exists or phone not provided
    """
    try:
        res = await service.revision.create(
            revision=revision,
            session=session,
            token=token,
            note_id=note_id
        )
    except ServiceException as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    except Exception as e:
        logger.error(f'got unexpected exception e={e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )
    else:
        if res is not None:
            return res
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="revision was not created",
        )


@router.get("/notes/{note_id}/revision")
async def get_revision(
        note_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> RevisionShortInfo:
    try:
        res = await service.revision.get(
            note_id=note_id,
            session=session,
        )
    except ServiceException as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    except Exception as e:
        logger.error(f'got unexpected exception e={e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error",
        )
    else:
        if res is not None:
            return res
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="revision was not created",
        )
