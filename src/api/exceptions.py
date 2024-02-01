from fastapi import status
from structlog import get_logger

logger = get_logger()


class ServiceException(BaseException):
    def __init__(
            self,
            code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail: str | None = None,
            log: str | None = None
    ):
        self.__code = code
        self.__detail = detail or "Internal server error"
        if log:
            logger.error(log, code=code, detail=detail)

        super().__init__(self.__detail)

    @property
    def code(self) -> int:
        return self.__code

    @property
    def detail(self) -> str:
        return self.__detail
