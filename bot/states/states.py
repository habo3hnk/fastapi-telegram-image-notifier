from aiogram.fsm.state import State, StatesGroup


class ImgForm(StatesGroup):
    waiting_for_image = State()
    waiting_for_title = State()
