from aiogram.types import CallbackQuery
from loguru import logger

from loader import dp, db


@dp.callback_query_handler(text="en")
async def chosen_english(call: CallbackQuery):
    user_id = call.from_user.id

    await db.change_language(user_id, 'en')
    await call.answer(text='✅ Changed')

    await call.message.delete()

    logger.info(f'{user_id} - Language changed to English')
