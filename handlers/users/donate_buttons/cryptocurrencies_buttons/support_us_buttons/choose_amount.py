from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from data.config import CRYPTO_PAY_URL, CRYPTO_PAY_API_TOKEN
from keyboards.inline import confirm_pay_amount_keyboard
from keyboards.inline.callback_data import choosing_cryptocurrency_callback
from keyboards.inline.cancel_button import cancel_button
from loader import dp, _
from utils.misc import CryptoPay


@dp.callback_query_handler(choosing_cryptocurrency_callback.filter(), state='Donate_SupportUs')
async def choose_amount(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Getting cryptocurrency exchange rate"""

    await call.answer(cache_time=1)
    crypto_currency = callback_data['currency']

    crypto_pay = CryptoPay(url=CRYPTO_PAY_URL, api_key=CRYPTO_PAY_API_TOKEN)
    exchange_rate = await crypto_pay.get_exchange_rate(source=crypto_currency)  # Getting cryptocurrency exchange rate

    await call.message.edit_text(_('<b>✅ {currency} currency selected\n'
                                   '📈 1$ - {exchange_rate} {currency}\n\n'
                                   '⬇ Write the donation amount in $0.5-500 below</b>').format(currency=crypto_currency,
                                                                                           exchange_rate=exchange_rate),
                                 reply_markup=InlineKeyboardMarkup(row_width=1,
                                                                   inline_keyboard=[
                                                                       [cancel_button]
                                                                   ]))
    await state.finish()
    await state.set_state('GetAmountDonate')
    await state.update_data(currency=crypto_currency)


@dp.message_handler(state='GetAmountDonate')
async def confirm_amount(message: Message, state: FSMContext):
    """Confirming donate amount"""

    data = await state.get_data()
    currency = data.get("currency")

    try:
        amount = float(message.text)

        if amount < 0.5 or amount > 5000:
            await message.answer(_('‼ <b>Enter an amount within $0.5-5000</b>'))
        else:
            await state.finish()
            await message.answer(_('<b>Confirm the payment amount or cancel the action:</b>\n\n'
                                   '<b>Currency:</b> {currency}\n'
                                   '<b>Amount:</b> ${amount}').format(amount=amount, currency=currency),
                                 reply_markup=confirm_pay_amount_keyboard)
            await state.set_state('ConfirmPayAmount')
            await state.update_data(currency=currency, amount=amount, is_paid_subscription=False)
    except ValueError:
        await message.answer(_('‼ <b>Enter amount. For example: 1, 0.7, 55.4</b>'))
