from aiogram.types import CallbackQuery

from loader import dp, _


@dp.callback_query_handler(text="cancel")
async def cancel(call: CallbackQuery):
    await call.answer(text=_('✅ Canceled'))
    await call.message.delete()



