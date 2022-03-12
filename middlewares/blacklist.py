from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class SetBlacklist(BaseMiddleware):
    """Tracker of user last action"""
    async def on_process_message(self, message: types.Message, data: dict):
        from loader import db

        user_id = message.from_user.id
        is_banned = await db.get_user_from_blacklist(user_id)

        if is_banned:
            raise CancelHandler()

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        from loader import db

        user_id = cq.from_user.id
        is_banned = await db.get_user_from_blacklist(user_id)

        if is_banned:
            raise CancelHandler()
