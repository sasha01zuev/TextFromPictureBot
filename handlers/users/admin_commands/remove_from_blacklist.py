import asyncpg
from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS_ID, MAIN_ADMIN
from loader import dp, db
from loguru import logger


@dp.message_handler(Command('rufb'), user_id=ADMINS_ID)
async def remove_user_from_blacklist(message: types.Message):
    """Removing users from blacklist"""

    user_id = message.get_args()
    admin_id = message.from_user.id
    admin_username = message.from_user.username
    admin_fullname = message.from_user.full_name

    try:
        user_id = int(user_id)
        in_blacklist = await db.get_user_from_blacklist(user_id)

        if in_blacklist:  # If user in blacklist
            await db.remove_user_from_blacklist(user_id)
            await message.answer('Успешно удален из чёрного списка!')
        else:  # If user not in blacklist
            await message.answer('Данного пользователя нету в чёрном списке!')
    except Exception as err:
        await message.answer(f"Ошибка!\n"
                             f"Следуй шаблону: /rufb [user_id]")
        logger.exception(f"Ошибка при удалении {user_id} из чёрного списка "
                         f"админом {admin_id} {admin_username} {admin_fullname}\n"
                         f"Подробнее:\n"
                         f"{err}")