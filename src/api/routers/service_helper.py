from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.service import Service
from src.api.storage.sql import get_storage
from src.core.models import db_helper


def get_service(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Service:
    """get_service is accessor to singleton service object"""

    return Service(get_storage(session))
