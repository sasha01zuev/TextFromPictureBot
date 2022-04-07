from aiogram import Dispatcher
from loguru import logger

from data.config import ADMINS_ID


async def on_startup_notify(dp: Dispatcher):
    """Notify admins on start up"""

    for admin in ADMINS_ID:
        try:
            await dp.bot.send_message(admin, "***Это сообщение видят только админы***\n"
                                             "БОТ ЗАПУЩЕН")
        except Exception as err:
            logger.exception(err)
