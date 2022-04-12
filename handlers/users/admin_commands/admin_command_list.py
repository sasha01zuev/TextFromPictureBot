from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS_ID, MAIN_ADMIN
from loader import dp


@dp.message_handler(Command('admin_command_list'), user_id=ADMINS_ID)
async def admin_command_list(message: types.Message):
    """Getting command list for admins"""

    user_id = message.from_user.id

    if int(user_id) == int(MAIN_ADMIN):
        await message.answer(
            '/mass_mailing - Рассылка всем пользователям\n'
            'Template: /mass_mailing (Audience: [ru/en/uk/all]) (Photo: [true/false]) '
            '(First_button(Optional): [Button_name-link]) (Second_button(Optional): '
            '[Button_name-link]) (Third_button(Optional): [Button_name-link])\n\n'
            '/autb - Добавить пользователя в черный список (Add User To Blacklist\n'
            'Template: /autb [user_id]\n\n'
            '/rufb - Удалить пользователя с чёрного списка (Remove User From Blacklist)\n'
            'Template: /rufb [user_id]\n\n'
            '/mtu - Отправить сообщение пользователю (Message To User)\n'
            'Template: /mtu [user_id]\n\n'
            '/get_logs - Получить файл с логами\n\n'
            '/get_user_info - Получить информацию о пользователе\n'
            'Template: /get_user_info [user_id]'
        )
    else:
        await message.answer(
            '/autb - Добавить пользователя в черный список (Add User To Blacklist\n'
            'Template: /autb [user_id]\n\n'
            '/rufb - Удалить пользователя с чёрного списка (Remove User From Blacklist)\n'
            'Template: /rufb [user_id]\n\n'
            '/mtu - Отправить сообщение пользователю (Message To User)\n'
            'Template: /mtu [user_id]\n\n'
            '/get_logs - Получить файл с логами\n\n'
            '/get_user_info - Получить информацию о пользователе\n'
            'Template: /get_user_info [user_id]'
        )
