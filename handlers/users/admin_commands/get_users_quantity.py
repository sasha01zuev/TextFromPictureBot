from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS_ID
from loader import dp, db


@dp.message_handler(Command('users_quantity'), user_id=ADMINS_ID)
async def get_users_quantity(message: types.Message):
    users_quantity = await db.get_users_quantity()
    await message.answer(f'Количество пользователей: {users_quantity}')
