from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import choosing_cryptocurrencies_keyboard
from keyboards.inline.choosing_paid_subscrption_plan import paid_subscription_plan_keyboard
from loader import dp, db, _


@dp.callback_query_handler(text="donate_paid_subscription")
async def support_us(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.edit_text(_('Choose a plan:'), reply_markup=paid_subscription_plan_keyboard)
    await state.set_state('Donate_PaidSubscription')
