import asyncio
from aiogram import Bot, Dispatcher, types, md
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import ImageGenerator
from DataSystem import log_user_action


class Form(StatesGroup):
    hello = State()
    menu = State()
    new_text = State()


async def start_handler(event: types.Message):
    
    with open("../../Downloads/ScrambleBot/static/gifs/testgif.gif", "rb") as gif:
        await event.answer_animation(gif, caption="Welcome to the Srcamble bot")
    await Form.menu.set()
    await menu_handler(event)
    log_user_action(event.from_user.username, "start")


async def menu_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="С пюрешкой")
    keyboard.add(button_1)
    button_2 = "Без пюрешки"
    keyboard.add(button_2)
    await message.answer("hello, welcome to menu", reply_markup=keyboard)
    await Form.new_text.set()
    log_user_action(message.from_user.username, "menu")
    

async def work_over_scramble(event: types.Message):
    visit_msg = "Wow, new scramble \n\nBy [scramblebot](http://t.me/scramb1er_bot)"
    with await ImageGenerator.get_scrambled(event.text) as gif:  # TODO: Md text
        await event.answer_animation(
            gif, 
            caption=visit_msg, 
            parse_mode=types.ParseMode.MARKDOWN 
        )
    log_user_action(event.from_user.username, "scramble")


async def main():
    bot = Bot(token=os.environ['tg_bot_key'])
    try:
        storage = MemoryStorage()
        disp = Dispatcher(bot=bot, storage=storage)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        disp.register_message_handler(work_over_scramble, state=Form.new_text)
        disp.register_message_handler(menu_handler, state=Form.menu)
        await disp.start_polling()
    finally:
        await bot.close()


def run():
    asyncio.run(main())
