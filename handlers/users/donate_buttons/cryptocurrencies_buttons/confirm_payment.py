from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import donate_keyboard, confirm_payment_keyboard
from loader import dp, _, bot
from utils.misc import CryptoPay
from data.config import CRYPTO_PAY_URL, CRYPTO_PAY_API_TOKEN


@dp.callback_query_handler(text='confirm_amount', state='ConfirmPayAmount')
async def confirm_amount(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    data = await state.get_data()
    currency = data.get("currency")
    amount = data.get("amount")

    get_bot = await bot.get_me()
    bot_username = get_bot.username

    bot_link = f'https://t.me/{bot_username}'
    await state.finish()

    crypto_pay = CryptoPay(url=CRYPTO_PAY_URL, api_key=CRYPTO_PAY_API_TOKEN)

    exchange_rate = await crypto_pay.get_exchange_rate(source=currency)
    crypto_amount = float(exchange_rate) * float(amount)

    invoice = await crypto_pay.create_invoice(asset=currency, amount=crypto_amount, paid_btn_name='callback',
                                    paid_btn_url=bot_link, allow_anonymous=False,
                                    description=_('Donation for the @{bot_username}').format(
                                        bot_username=bot_username),
                                    hidden_message=_('Thanks for the donation!'),
                                    expires_in=60)
    if invoice:
        invoice_id = invoice['result']['invoice_id']
        await crypto_pay.get_invoice(invoice_id)
        await call.message.edit_text(_('Confirm payment or cancel action\n\n'
                                       'Amount: ${amount} ({crypto_amount} {currency})\n'
                                       'Currency: {currency}').format(amount=amount, currency=currency,
                                                                      crypto_amount=crypto_amount),
                                     reply_markup=confirm_payment_keyboard)
        await state.set_state('PaymentConfirmed')
    else:
        # TODO обработать если нету
        print(invoice)


@dp.callback_query_handler(text='confirm_payment', state='PaymentConfirmed')
async def payment_confirmed(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    print('Confirmed')



