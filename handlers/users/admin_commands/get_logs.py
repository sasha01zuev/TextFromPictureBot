from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS_ID, MAIN_ADMIN
from loader import dp


@dp.message_handler(Command('get_logs'), user_id=ADMINS_ID)
async def admin_command_list(message: types.Message):
    """Getting logs"""
    try:
        await message.answer_document(types.InputFile(path_or_bytesio='info.log', filename='Logs'))
    except Exception as err:
        await message.answer(f'Ошибка при отправке логов:\n{err}')