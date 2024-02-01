from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.notes import GetAllNotesResponse
from src.core.models import db_helper
from .service_helper import service
from ..exceptions import ServiceException

router = APIRouter(
    tags=[
        "Users",
    ],
    prefix="/notes"
)


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
