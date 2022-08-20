import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import logging
from engine.handlers.controls import dispatcher_register_handlers

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=os.environ['tg_bot_key'])
    try:
        storage = MemoryStorage()
        dp = Dispatcher(bot=bot, storage=storage)
        await dispatcher_register_handlers(dp)
        await dp.start_polling()
    finally:
        await bot.close()


def run():
    asyncio.run(main())
