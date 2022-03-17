from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp, _


@dp.callback_query_handler(text="cancel")
async def cancel(call: CallbackQuery):
    await call.answer(text=_('✅ Canceled'))
    await call.message.delete()


@dp.callback_query_handler(text="cancel_mass_mailing")
async def confirm_mass_mailing(call: CallbackQuery):
    await call.answer(text='✅ Canceled')
    await call.message.delete()


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



