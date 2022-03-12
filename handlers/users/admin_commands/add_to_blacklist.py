import json

import asyncpg
from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS_ID, MAIN_ADMIN
from loader import dp, db
from loguru import logger


@dp.message_handler(Command('autb'), user_id=ADMINS_ID)
async def add_user_to_blacklist(message: types.Message):
    user_id = message.get_args()
    admin_id = message.from_user.id
    admin_username = message.from_user.username
    admin_fullname = message.from_user.full_name

    try:
        user_id = int(user_id)
        user = await db.get_user(user_id)

        if user:
            if user in ADMINS_ID and admin_id != MAIN_ADMIN:
                await message.answer('Ты не можешь блокировать администрацию')
            else:
                await db.add_user_to_blacklist(user_id)
                await message.answer('Успешно добавлено!')
                logger.info(f'{user_id} добавлен в чёрный список админом {admin_id} '
                            f'{admin_username} {admin_fullname}!')
        else:
            await message.answer('Не правильный ID пользователя')
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer('Пользователь уже добавлен в чёрный список!')
    except Exception as err:
        await message.answer(f"Ошибка!\n"
                             f"Следуй шаблону: /autb [user_id]")
        logger.exception(f"Ошибка при добавлении пользователя {user_id} в чёрный список "
                         f"админом {admin_id} {admin_username} {admin_fullname}\n"
                         f"Подробнее:\n"
                         f"{err}")
