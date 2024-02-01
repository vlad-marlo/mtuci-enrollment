from structlog import configure, get_logger
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

logger = get_logger()

if __name__ == "__main__":
    logger.warning("hello")
