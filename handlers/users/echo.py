from aiogram import types
from aiogram.types import ContentType, Message

from loader import dp


@dp.message_handler()
async def echo(message: types.Message):
    """Answer for simple message"""
    await message.answer("Не понял команды! 🤨😲")


