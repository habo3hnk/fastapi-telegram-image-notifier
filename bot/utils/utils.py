import os
import asyncio
from datetime import datetime
from aiogram.types import Message, PhotoSize
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from config.config import IMAGE_FOLDER, SERVER_URL, IMG_MAX_SIZE_MB
from bot.static.static_text import errors


async def save_img(bot: Bot, photo: PhotoSize) -> tuple[bool, str]:
    max_size_bytes = IMG_MAX_SIZE_MB * 1024 * 1024

    if not photo.file_size:
        return False, errors["img_not_size"]

    if photo.file_size > max_size_bytes:
        return False, errors["img_max_size"].format(size=IMG_MAX_SIZE_MB)

    try:
        file = await bot.get_file(photo.file_id)

        file_ext = os.path.splitext(file.file_path or "")[-1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{timestamp}{file_ext}"
        file_path = os.path.join(IMAGE_FOLDER, filename)

        if file.file_path:
            await bot.download_file(file.file_path, destination=file_path)
            return True, f"{SERVER_URL}/img/{filename}"
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
