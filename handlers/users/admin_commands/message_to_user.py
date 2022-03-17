import re

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from data.config import ADMINS_ID, MAIN_ADMIN

from keyboards.default import cancel_mtu_keyboard

from loader import dp, bot, db


@dp.message_handler(Command('mtu'), user_id=ADMINS_ID)
async def mtu(message: Message, state: FSMContext):
    try:
        user_id = int(message.get_args())
        user = await db.get_user(user_id)

        if user:
            await message.answer('Впиши ниже сообщение пользователю 🠓', reply_markup=cancel_mtu_keyboard)
            await state.set_state('ConfirmMessageToUser')
            await state.update_data(user_id=user_id)
        else:
            await message.answer("Не правильный ID юзера!")
    except:
        await message.answer('Введи правильно ID пользователя!')


@dp.message_handler(state='ConfirmMessageToUser')
async def send_message(message: Message, state: FSMContext):
    if message.text == "⬅ Отмена" or message.text.lower() == 'отм':
        await message.answer('❎ Отправка сообщения отменена!', reply_markup=ReplyKeyboardRemove())
    else:
        data = await state.get_data()
        user_id = data.get("user_id")

        try:
            await bot.send_message(int(user_id), f"<i>АДМИНИСТРАЦИЯ</i>\n\n{message.text}")
            await message.answer('✅ Сообщение успешно доставлено!')
        except Exception as err:
            await message.answer(f'Скорее всего пользователь заблокировал бота.\nОшибка: \n\n{err}')
    await state.finish()
