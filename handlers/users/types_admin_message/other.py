from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, _
from states import ConfirmMsgToAdmin


@dp.callback_query_handler(text="other")
async def message_type(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.edit_text(_('<b>Input message below ⬇</b>'))
    await ConfirmMsgToAdmin.SetMessageType.set()
    await state.update_data(type='Другое')
