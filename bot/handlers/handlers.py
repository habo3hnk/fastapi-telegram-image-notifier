from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.callback_data import CallbackData
from keyboards.main_menu import get_main_keyboard
from static.static_text import main_menu


main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text=main_menu["main"],
        reply_markup=get_main_keyboard(),
    )


@main_router.callback_query(F.data == CallbackData.GET_IMG_LIST.value)
async def handle_get_img_list_btn(callback: CallbackQuery):
    await callback.answer("JOPA")


# NOTE: Надо будет сделать рефакторинг структуры handlers. Мб сделаю
# Отдельный модуль для обработки комман.
