from aiogram.types import CallbackQuery
from loguru import logger

from loader import dp, db, _


@dp.callback_query_handler(text="uk")
async def chosen_russian(call: CallbackQuery):
    user_id = call.from_user.id

    await db.change_language(user_id, 'uk')
    await call.answer(text='✅ Змінено')
    await call.message.delete()

    logger.info(f'{user_id} - Language changed to Ukrainian')
