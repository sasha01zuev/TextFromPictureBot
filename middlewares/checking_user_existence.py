from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import db


class CheckingUserExistence(BaseMiddleware):
    """Tracker of user last action"""
    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        user = await db.get_user(user_id)

        if user or '/start' in message.text:
            pass
        else:
            await message.answer('Нажмите /start !')
            raise CancelHandler()

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user_id = cq.from_user.id

        user = await db.get_user(user_id)

        if user or cq.message.text == '/start':
            pass
        else:
            await cq.message.answer('Нажмите /start !')
            raise CancelHandler()
