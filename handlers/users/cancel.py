from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import donate_keyboard
from loader import dp, _
import os

"""Functions for cancel button and finishing states"""


@dp.callback_query_handler(text="cancel")
async def cancel(call: CallbackQuery):
    await call.answer(cache_time=1, text=_('✅ Canceled'))
    await call.message.delete()


@dp.callback_query_handler(text="cancel_mass_mailing")
async def confirm_mass_mailing(call: CallbackQuery):
    await call.answer(cache_time=1, text=_('✅ Canceled'))
    await call.message.delete()


@dp.callback_query_handler(text='cancel', state='ConfirmLangPhotoText')
async def confirm_language_photo_text(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1, text=_('✅ Canceled'))
    await call.message.delete()

    state_data = await state.get_data()
    photo_path = state_data.get('photo_path')
    os.remove(photo_path)

    await state.finish()


@dp.callback_query_handler(text="cancel_mass_mailing", state="ConfirmingTextMessage")
async def confirm_mass_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1, text=_('✅ Canceled'))
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text="cancel_mass_mailing", state="ConfirmingPhotoTextMessage")
async def confirm_mass_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1, text=_('✅ Canceled'))
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='cancel', state='Donate_SupportUs')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()

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
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='Donate_PaidSubscription')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()

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
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='GetAmountDonate')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()

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
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='PaidSubscription_Cryptocurrency')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()

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
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='ConfirmPayAmount')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()

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
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='PaymentConfirmed')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.finish()

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
          'more servers - less load'), reply_markup=donate_keyboard)
