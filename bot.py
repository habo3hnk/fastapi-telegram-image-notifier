import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import TOKEN
from bot.handlers import router
from bot.middlewares.db import DbSessionMiddleware


def setup_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def create_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    return dp


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = create_dispatcher()
    dp.update.middleware(DbSessionMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
