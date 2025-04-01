from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database import database


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self):
        self.session_pool = database

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool.session() as session:
            data["session"] = session
            return await handler(event, data)
