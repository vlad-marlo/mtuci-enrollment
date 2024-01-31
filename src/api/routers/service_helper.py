from sqlalchemy.ext.asyncio import AsyncSession

from src.api.service import Service
from src.api.storage.sql import get_storage
from src.core.models import db_helper

__service = Service(get_storage(db_helper.get_scoped_session()))


def get_service(session: AsyncSession) -> Service:
    __service.replace_session(session)
    return __service
