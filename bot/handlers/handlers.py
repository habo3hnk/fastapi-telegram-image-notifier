from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.callback_data import CallbackData
from bot.keyboards.main_menu import get_main_keyboard
from bot.static.static_text import main_menu
from database.crud import get_user_by_telegram_id, create_user, get_images_by_user


main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    if not message.from_user:
        return

    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(session=session, telegram_id=telegram_id)

    if not user:
        user = await create_user(session=session, telegram_id=telegram_id)

    await state.clear()
    await message.answer(
        text=main_menu["main"],
        reply_markup=get_main_keyboard(),
    )


@main_router.callback_query(F.data == CallbackData.GET_IMG_LIST.value)
async def handle_get_img_list_btn(callback: CallbackQuery, session: AsyncSession):
    # TODO: Тут надо будет добавить клавиатуру с выбором конкретного изображения
    # и хендлер этот переместить в другое место

    telegram_id = callback.from_user.id
    user = await get_user_by_telegram_id(session=session, telegram_id=telegram_id)

    imgs = await get_images_by_user(session=session, user_id=user.id)

    for i in imgs:
        await callback.message.answer(text=i.file_name)


# NOTE: Надо будет сделать рефакторинг структуры handlers. Мб сделаю
# Отдельный модуль для обработки комманд.
