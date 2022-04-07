from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class SetBlacklist(BaseMiddleware):
    """Middleware class if user in blacklist"""

    async def on_process_message(self, message: types.Message, data: dict):
        from loader import db, bot, _

        user_id = message.from_user.id
        is_banned = await db.get_user_from_blacklist(user_id)

        if is_banned:
            await bot.send_message(user_id, _('You have been banned! Contact @Sasha_Zuev'))
            raise CancelHandler()

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        from loader import db, bot, _

        user_id = cq.from_user.id
        is_banned = await db.get_user_from_blacklist(user_id)

        if is_banned:
            await bot.send_message(user_id, _('You have been banned! Contact @Sasha_Zuev'))
            raise CancelHandler()
