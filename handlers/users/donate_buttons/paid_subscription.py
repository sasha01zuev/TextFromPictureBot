from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.choosing_paid_subscrption_plan import paid_subscription_plan_keyboard
from loader import dp, _


@dp.callback_query_handler(text="donate_paid_subscription")
async def support_us(call: CallbackQuery, state: FSMContext):
    """If chosen 'Paid subscription' while donate"""

    await call.answer(cache_time=1)
    await call.message.edit_text(_('<b>Choose a plan:</b>'), reply_markup=await paid_subscription_plan_keyboard())
    await state.set_state('Donate_PaidSubscription')
