from aiogram.types import CallbackQuery

from loader import dp
from keyboards.inline import bg_color_keyboard, l_language_keyboard
from keyboards.inline.callback_data import bg_color_callback


@dp.callback_query_handler(bg_color_callback.filter(color='light'))
async def selecting_language(call: CallbackQuery):
    """Selecting language text from picture"""
    await call.answer(cache_time=5)
    await call.message.delete()
    await call.message.answer("Choose language from picture:",  reply_markup=l_language_keyboard)
