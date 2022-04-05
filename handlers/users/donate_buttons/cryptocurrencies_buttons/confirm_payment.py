from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import donate_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, db, _, bot
from utils.misc import CryptoPay
from data.config import CRYPTO_PAY_URL, CRYPTO_PAY_API_TOKEN


@dp.callback_query_handler(text='confirm_amount', state='ConfirmPayAmount')
async def confirm_amount(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    data = await state.get_data()
    currency = data.get("currency")
    amount = data.get("amount")
    is_paid_subscription = data.get('is_paid_subscription')

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
                                    expires_in=60)

    if invoice:
        invoice_id = invoice['invoice_id']
        pay_url = invoice['pay_url']

        confirm_payment_keyboard = InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔗 Pay", url=pay_url)
                ],
                [
                    InlineKeyboardButton(text="✅ Paid",
                                         callback_data='confirm_payment'),
                    cancel_button
                ]

            ]
        )

        await call.message.edit_text(_('Confirm payment or cancel action\n\n'
                                       'Amount: ${amount} ({crypto_amount} {currency})\n'
                                       'Currency: {currency}').format(amount=amount, currency=currency,
                                                                      crypto_amount=crypto_amount),
                                     reply_markup=confirm_payment_keyboard)
        await state.set_state('PaymentConfirmed')
        await state.update_data(invoice_id=invoice_id, is_paid_subscription=is_paid_subscription,
                                amount=amount, currency=currency)
    else:
        await state.finish()
        await call.message.edit_text(_('Unknown error while generating invoice!'))
        await call.message.answer(
            _('To support us or get a paid subscription, you need to register in the official telegram '
              'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
              '- If you chose "support us" -- you can choose any amount to donate\n\n'
              '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
              '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
              'more servers - less load\n'
              '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
              'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='confirm_payment', state='PaymentConfirmed')
async def payment_confirmed(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    crypto_pay = CryptoPay(url=CRYPTO_PAY_URL, api_key=CRYPTO_PAY_API_TOKEN)
    data = await state.get_data()
    invoice_id = data.get("invoice_id")
    amount = str(data.get('amount'))
    currency = data.get('currency')
    is_paid_subscription = data.get('is_paid_subscription')

    paid_invoice = await crypto_pay.get_paid_invoice(invoice_id)
    try:
        comment = paid_invoice[0]['comment']
    except KeyError:
        comment = None
    except TypeError:
        comment = None

    print(paid_invoice)

    if paid_invoice:
        await call.message.edit_text(_('Thanks for donation!'))
        if is_paid_subscription:
            await db.add_user_donate(user_id=user_id, amount=amount, currency=currency, message=comment)
            await db.add_user_subscription(user_id=user_id, date_to=amount)
        else:
            await db.add_user_donate(user_id=user_id, amount=amount, currency=currency, message=comment)
        await state.finish()
    else:
        await call.answer(text=_('Not paid!'))





