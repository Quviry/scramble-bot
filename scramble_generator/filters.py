from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    start = State()
    menu = State()
    enter_text_single_menu = State()
    enter_text_single_render = State()

