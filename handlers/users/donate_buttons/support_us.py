from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import choosing_cryptocurrencies_keyboard
from loader import dp, db, _


@dp.callback_query_handler(text="donate_support")
async def support_us(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.edit_text(_('Choose a cryptocurrency:'), reply_markup=choosing_cryptocurrencies_keyboard)
    await state.set_state('Donate_SupportUs')