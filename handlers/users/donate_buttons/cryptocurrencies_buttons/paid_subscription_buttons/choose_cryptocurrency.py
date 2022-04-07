from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import choosing_cryptocurrencies_keyboard, confirm_pay_amount_keyboard
from keyboards.inline.callback_data import choosing_paid_subscription_plan_callback, choosing_cryptocurrency_callback
from loader import dp, _


@dp.callback_query_handler(choosing_paid_subscription_plan_callback.filter(), state='Donate_PaidSubscription')
async def paid_subscription(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Choosing cryptocurrency"""

    await call.answer(cache_time=1)
    amount = callback_data['amount']
    await call.message.edit_text(_('Choose a cryptocurrency:'), reply_markup=choosing_cryptocurrencies_keyboard)
    await state.set_state('PaidSubscription_Cryptocurrency')
    await state.update_data(amount=amount)


@dp.callback_query_handler(choosing_cryptocurrency_callback.filter(), state='PaidSubscription_Cryptocurrency')
async def choosing_cryptocurrency(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Confirming paid subscription plan"""

    await call.answer(cache_time=1)
    data = await state.get_data()
    amount = data.get('amount')
    currency = callback_data['currency']

    await state.finish()

    await call.message.edit_text(_('Confirm your subscription plan or cancel the action:\n\n'
                                   'Currency: {currency}\n'
                                   'Amount: ${amount}').format(amount=amount, currency=currency),
                                 reply_markup=confirm_pay_amount_keyboard)
    await state.set_state('ConfirmPayAmount')
    await state.update_data(currency=currency, amount=amount, is_paid_subscription=True)
