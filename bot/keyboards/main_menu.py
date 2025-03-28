from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import CallbackData
from static.static_text import buttons


def get_main_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text=buttons["new_img_btn"], callback_data=CallbackData.CREATE_IMAGE.value
    )
    builder.button(
        text=buttons["my_img_btn"], callback_data=CallbackData.GET_IMG_LIST.value
    )

    builder.adjust(1)

    return builder.as_markup()


def get_chanel_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text=buttons["cancel_btn"], callback_data=CallbackData.CANCEL.value)

    builder.adjust(1)

    return builder.as_markup()
