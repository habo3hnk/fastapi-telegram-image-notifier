import os
import asyncio
from datetime import datetime
from aiogram.types import Message, PhotoSize
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession
from config.config import IMAGE_FOLDER, SERVER_URL, IMG_MAX_SIZE_MB
from bot.static.static_text import errors
from database.crud import create_image, get_user_by_telegram_id

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import TOKEN


def get_bot() -> Bot:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    return bot


async def save_img(
    bot: Bot,
    session: AsyncSession,
    telegram_id: int,
    display_name: str,
    photo: PhotoSize,
) -> tuple[bool, str]:
    max_size_bytes = IMG_MAX_SIZE_MB * 1024 * 1024

    if not photo.file_size:
        return False, errors["img_not_size"]

    if photo.file_size > max_size_bytes:
        return False, errors["img_max_size"].format(size=IMG_MAX_SIZE_MB)

    try:
        file = await bot.get_file(photo.file_id)

        file_ext = os.path.splitext(file.file_path or "")[-1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_name = f"{timestamp}{file_ext}"
        file_path = os.path.join(IMAGE_FOLDER, file_name)

        if file.file_path:
            await bot.download_file(file.file_path, destination=file_path)

            user = await get_user_by_telegram_id(
                session=session, telegram_id=telegram_id
            )
            if user:
                await create_image(
                    session=session,
                    user_id=user.id,
                    file_name=file_name,
                    display_name=display_name,
                )

                return True, f"{SERVER_URL}/img/{file_name}"
        return False, "error_text"
    except Exception as e:
        print(e)
        return False, errors["default"]


async def delete_message(message: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except TelegramBadRequest as e:
        raise e


async def delete_message_by_id(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest as e:
        raise e
