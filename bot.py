import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import router
from bot.middlewares.db import DbSessionMiddleware
from bot.utils.utils import get_bot


def setup_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def create_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    return dp


async def main() -> None:
    bot = get_bot()

    dp = create_dispatcher()
    dp.update.middleware(DbSessionMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
