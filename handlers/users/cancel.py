from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import donate_keyboard
from loader import dp, _
import os


@dp.callback_query_handler(text="cancel")
async def cancel(call: CallbackQuery):
    await call.answer(text=_('✅ Canceled'))
    await call.message.delete()


@dp.callback_query_handler(text="cancel_mass_mailing")
async def confirm_mass_mailing(call: CallbackQuery):
    await call.answer(text='✅ Canceled')
    await call.message.delete()


@dp.callback_query_handler(text='cancel', state='ConfirmLangPhotoText')
async def confirm_language_photo_text(call: CallbackQuery, state: FSMContext):
    await call.answer(text='✅ Canceled')
    await call.message.delete()

    state_data = await state.get_data()
    photo_path = state_data.get('photo_path')
    os.remove(photo_path)

    await state.finish()


@dp.callback_query_handler(text="cancel_mass_mailing", state="ConfirmingTextMessage")
async def confirm_mass_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(text='✅ Canceled')
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text="cancel_mass_mailing", state="ConfirmingPhotoTextMessage")
async def confirm_mass_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer(text='✅ Canceled')
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(text='cancel', state='Donate_SupportUs')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()

    await call.message.edit_text(
        _('To support us or get a paid subscription, you need to register in the official telegram '
          'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
          '- If you chose "support us" -- you can choose any amount to donate\n\n'
          '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
          '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
          'more servers - less load\n'
          '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='Donate_PaidSubscription')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()

    await call.message.edit_text(
        _('To support us or get a paid subscription, you need to register in the official telegram '
          'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
          '- If you chose "support us" -- you can choose any amount to donate\n\n'
          '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
          '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
          'more servers - less load\n'
          '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='GetAmountDonate')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()

    await call.message.edit_text(
        _('To support us or get a paid subscription, you need to register in the official telegram '
          'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
          '- If you chose "support us" -- you can choose any amount to donate\n\n'
          '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
          '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
          'more servers - less load\n'
          '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='PaidSubscription_Cryptocurrency')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()

    await call.message.edit_text(
        _('To support us or get a paid subscription, you need to register in the official telegram '
          'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
          '- If you chose "support us" -- you can choose any amount to donate\n\n'
          '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
          '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
          'more servers - less load\n'
          '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='ConfirmPayAmount')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()

    await call.message.edit_text(
        _('To support us or get a paid subscription, you need to register in the official telegram '
          'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
          '- If you chose "support us" -- you can choose any amount to donate\n\n'
          '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
          '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
          'more servers - less load\n'
          '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
          'more servers - less load'), reply_markup=donate_keyboard)


@dp.callback_query_handler(text='cancel', state='PaymentConfirmed')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()

    await call.message.edit_text(
        _('To support us or get a paid subscription, you need to register in the official telegram '
          'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
          '- If you chose "support us" -- you can choose any amount to donate\n\n'
          '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
          '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
          'more servers - less load\n'
          '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
          'more servers - less load'), reply_markup=donate_keyboard)
