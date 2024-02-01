from structlog import configure
from structlog.processors import (
    JSONRenderer,
    add_log_level,
    EventRenamer,
    StackInfoRenderer,
    TimeStamper,
)


configure(
    processors=[
        TimeStamper(fmt="iso"),
        add_log_level,
        EventRenamer("msg"),
        StackInfoRenderer(),
        JSONRenderer(),
    ],
)
if __name__ == "__main__":
    from structlog import get_logger

    logger = get_logger()
    logger.warning("hello")
