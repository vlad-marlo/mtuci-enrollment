from asyncio import Lock
from typing import Callable


def with_lock(lock: Lock = Lock()):
    async def wrapper(function: Callable):
        async def inner(*args, **kwargs):
            async with lock:
                res = function(*args, **kwargs)
            return res

        return inner

    return wrapper
