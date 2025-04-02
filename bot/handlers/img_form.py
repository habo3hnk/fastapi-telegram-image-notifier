import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, user
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.main_menu import get_chanel_keyboard, get_main_keyboard
from bot.keyboards.callback_data import CallbackData
from bot.states.states import ImgForm
from bot.static.static_text import main_menu, img_form, errors
from bot.utils.utils import delete_message, delete_message_by_id, save_img
from aiogram import Bot


img_router = Router()


@img_router.callback_query(F.data == CallbackData.CREATE_IMAGE.value)
async def image_creation_start(callback: CallbackQuery, state: FSMContext):
    keyboard = get_chanel_keyboard()
    await state.set_state(ImgForm.waiting_for_image)

    if isinstance(callback.message, Message):
        await state.update_data(last_message_id=callback.message.message_id)
        await callback.message.edit_text(
            text=img_form["upload_img"], reply_markup=keyboard
        )


@img_router.message(StateFilter(ImgForm.waiting_for_image), F.photo)
async def image_upload(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
):
    if not message.from_user:
        return

    data = await state.get_data()
    photo = message.photo

    if not isinstance(photo, list):
        await message.delete()
        warning_message = await message.answer(errors["default"])
        asyncio.create_task(delete_message(message=warning_message, delay=10))
        return

    telegram_id = message.from_user.id
    display_name = ""

    if message.caption:
        display_name = message.caption

    success, result_msg = await save_img(
        bot=bot,
        session=session,
        telegram_id=telegram_id,
        display_name=display_name,
        photo=photo[-1],
    )

    if success:
        await message.answer(result_msg)

        keyboard = get_main_keyboard()
        await message.answer(text=main_menu["main"], reply_markup=keyboard)

        chat_id = 0
        if message.from_user:
            chat_id = message.from_user.id

        await delete_message_by_id(
            bot=bot, message_id=data["last_message_id"], chat_id=chat_id
        )
        await state.clear()

    else:
        await message.delete()
        warning_message = await message.answer(result_msg)
        asyncio.create_task(delete_message(message=warning_message, delay=10))


@img_router.callback_query(F.data == CallbackData.CANCEL.value)
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    keyboard = get_main_keyboard()

    if isinstance(callback.message, Message):
        await callback.message.edit_text(text=main_menu["main"], reply_markup=keyboard)
