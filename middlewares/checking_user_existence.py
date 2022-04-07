from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class CheckingUserExistence(BaseMiddleware):
    """Checking user existence in database"""
    async def on_process_message(self, message: types.Message, data: dict):
        from loader import db, _
        user_id = message.from_user.id
        user = await db.get_user(user_id)

        if not message.text:
            if user:
                pass
            else:
                await message.answer(_('Press /start !'))
                raise CancelHandler()
        else:
            if user or '/start' in message.text:
                pass
            else:
                await message.answer(_('Press /start !'))
                raise CancelHandler()

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        from loader import db, _
        user_id = cq.from_user.id

        user = await db.get_user(user_id)

        if user or cq.message.text == '/start':
            pass
        else:
            await cq.message.answer(_('Press /start !'))
            raise CancelHandler()
