from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline import donate_keyboard, confirm_payment_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, db, _, bot
from utils.misc import CryptoPay
from data.config import CRYPTO_PAY_URL, CRYPTO_PAY_API_TOKEN
from loguru import logger


@dp.callback_query_handler(text='confirm_amount', state='ConfirmPayAmount')
async def confirm_amount(call: CallbackQuery, state: FSMContext):
    """Creating payment invoice"""

    await call.answer(cache_time=1)
    user_id = call.from_user.id
    data = await state.get_data()
    currency = data.get("currency")
    amount = data.get("amount")
    is_paid_subscription = data.get('is_paid_subscription')

    get_bot = await bot.get_me()
    bot_username = get_bot.username

    bot_link = f'https://t.me/{bot_username}'
    await state.finish()

    crypto_pay = CryptoPay(url=CRYPTO_PAY_URL, api_key=CRYPTO_PAY_API_TOKEN)

    exchange_rate = await crypto_pay.get_exchange_rate(source=currency)  # Getting cryptocurrency exchange rate
    crypto_amount = float(exchange_rate) * float(amount)

    invoice = await crypto_pay.create_invoice(asset=currency, amount=crypto_amount, paid_btn_name='callback',
                                              paid_btn_url=bot_link, allow_anonymous=False,
                                              description=_('Donation for the @{bot_username}').format(
                                                  bot_username=bot_username),
                                              expires_in=60)  # Creating invoice

    if invoice:  # If invoice was created successfully
        invoice_id = invoice['invoice_id']
        pay_url = invoice['pay_url']

        await call.message.edit_text(_('<b>Confirm payment or cancel action</b>\n\n'
                                       '<b>Amount</b>: ${amount} ({crypto_amount} {currency})\n'
                                       '<b>Currency</b>: {currency}').format(amount=amount, currency=currency,
                                                                      crypto_amount=crypto_amount),
                                     reply_markup=await confirm_payment_keyboard(pay_url=pay_url))
        await state.set_state('PaymentConfirmed')
        await state.update_data(invoice_id=invoice_id, is_paid_subscription=is_paid_subscription,
                                amount=amount, currency=currency)
        logger.info(f'{user_id} - Invoice created\n'
                    f'Invoice: {invoice}\n'
                    f'Paid subscription: {is_paid_subscription}\n'
                    f'Currency: {currency}\n'
                    f'Amount: ${amount}\n'
                    f'1$ - {exchange_rate}')

    else:  # If error while creating invoice
        await state.finish()
        await call.message.edit_text(_('Unknown error while generating invoice!'))
        await call.message.edit_text(
            _('<b>To support us or get a paid subscription, '
              'you need to register in the official telegram '
              'crypto wallet bot - @CryptoBot and top up your wallet</b>\n\n'
              '✅ If you chosen "<b>Support us</b>" — you can choose any amount to donate\n\n'
              '✅ If you have chosen "<b>Paid subscription</b>" — '
              'you can choose several types of subscription:\n'
              '    · <b>30$/month</b> — 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
              'more servers - less load\n'
              '    · <b>60$/month</b> — 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
              'more servers - less load'), reply_markup=await donate_keyboard())
        logger.error(f'{user_id} - Invoice NOT created\n'
                     f'Paid subscription: {is_paid_subscription}\n'
                     f'Currency: {currency}\n'
                     f'Amount: ${amount}\n'
                     f'1$ - {exchange_rate}')


@dp.callback_query_handler(text='confirm_payment', state='PaymentConfirmed')
async def payment_confirmed(call: CallbackQuery, state: FSMContext):
    """Confirming payment. Adding payment to database"""

    user_id = call.from_user.id

    data = await state.get_data()
    invoice_id = data.get("invoice_id")
    amount = str(data.get('amount'))
    currency = data.get('currency')
    is_paid_subscription = data.get('is_paid_subscription')

    crypto_pay = CryptoPay(url=CRYPTO_PAY_URL, api_key=CRYPTO_PAY_API_TOKEN)
    paid_invoice = await crypto_pay.get_paid_invoice(invoice_id)

    try:  # If comment was added to payment
        comment = paid_invoice[0]['comment']
    except KeyError:
        comment = None
    except TypeError:
        comment = None

    if paid_invoice:  # If invoice was paid
        await call.message.edit_text(_('<b>THANKS FOR DONATION!</b>'))
        if is_paid_subscription:  # If paid for paid subscription
            await db.add_user_donate(user_id=user_id, amount=amount, currency=currency, message=comment)
            await db.add_user_subscription(user_id=user_id, date_to=amount)
            logger.success(f'{user_id} - Invoice PAID\n'
                           f'Invoice: {paid_invoice}\n'
                           f'Paid subscription: {is_paid_subscription}\n'
                           f'Currency: {currency}\n'
                           f'Amount: ${amount}')
        else:  # If paid for donation
            await db.add_user_donate(user_id=user_id, amount=amount, currency=currency, message=comment)
            logger.success(f'{user_id} - Invoice PAID\n'
                           f'Invoice: {paid_invoice}\n'
                           f'Paid subscription: {is_paid_subscription}\n'
                           f'Currency: {currency}\n'
                           f'Amount: ${amount}')
        await state.finish()
    else:
        await call.answer(cache_time=1, text=_('Not paid!'))
        logger.info(f'{user_id} - Invoice NOT PAID\n'
                    f'Invoice: {paid_invoice}\n'
                    f'Paid subscription: {is_paid_subscription}\n'
                    f'Currency: {currency}\n'
                    f'Amount: ${amount}')
