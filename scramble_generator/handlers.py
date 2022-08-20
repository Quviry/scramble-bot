from aiogram import types
from .filters import UserState
from . import ImageGenerator
from logging import getLogger
from aiogram import Dispatcher

logger = getLogger(__name__)


async def start_handler(event: types.Message):
    logger.debug("Start handler")
    with open("static/gifs/testgif.gif", "rb") as gif:
        await event.answer_animation(gif, caption="Welcome to the Srcamble bot")
    await UserState.menu.set()
    await menu_handler(event)


async def menu_handler(message: types.Message):
    logger.debug("Menu handler")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    settings_btn = types.InlineKeyboardButton(text="Настройки", callback_data="setsettingsstate")
    render_string_btn = types.InlineKeyboardButton(text="Рендер строки", callback_data="setstringstate")
    render_strings_btn = types.InlineKeyboardButton(text="Рендер нескольких строк", callback_data="setstringsstate")
    keyboard.add(settings_btn, render_string_btn, render_strings_btn)
    await message.answer("hello, welcome to menu", reply_markup=keyboard)


async def work_over_scramble(event: types.Message):
    logger.debug("Scramble Handler")
    visit_msg = "Wow, new scramble \n\nBy [scramblebot](http://t.me/scramb1er_bot)"
    with await ImageGenerator.get_scrambled(event.text) as gif:
        await event.reply_animation(
            gif,
            caption=visit_msg,
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=types.ReplyKeyboardRemove()
        )
    await UserState.enter_text_single_menu.set()
    await enter_string_handler(event)
    #  log_user_action(event.from_user.username, "scramble")


async def enter_string_handler(event: types.Message):
    logger.debug('enter_string_handler')
    msg = 'Enter new string'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='cancel'))
    await event.answer('Введите текст для рендера', reply_markup=keyboard)
    await UserState.enter_text_single_render.set()


async def return_to_menu(call: types.CallbackQuery):
    logger.error("fuck this callbacks")
    await UserState.menu.set()
    await menu_handler(call.message)
    await call.answer(cache_time=60)


async def set_string_state_callback(call: types.CallbackQuery):
    logger.error('set_string_state_callback')
    await UserState.enter_text_single_menu.set()
    await enter_string_handler(call.message)
    await call.answer(cache_time=60)


async def resolve_query(call: types.CallbackQuery):
    print('who')
    await call.bot.answer_callback_query(call.id, text=call.data)


async def register_handlers(dp: Dispatcher, *args, **kwargs):
    """ function with reserved name that register handlers for engine """
    logger.debug("Registering animation handlers")

    dp.register_callback_query_handler(set_string_state_callback, text='setstringstate', state=UserState.menu)
    dp.register_callback_query_handler(return_to_menu, text='cancel', state=UserState.enter_text_single_render)

    dp.register_message_handler(start_handler, commands={'start', 'restart'}, state='*')

    dp.register_message_handler(enter_string_handler, state=UserState.enter_text_single_menu)
    dp.register_message_handler(menu_handler, state=UserState.menu)
    dp.register_message_handler(work_over_scramble, state=UserState.enter_text_single_render)

    dp.register_message_handler(start_handler, state='*')
