from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import language_callback
from loader import dp


@dp.callback_query_handler(language_callback.filter(lang='d_rus'))
async def selecting_language(call: CallbackQuery):
    """Selecting background color from pic"""
    await call.answer(cache_time=5)
    await call.message.delete()
    await call.message.answer("Привет")
