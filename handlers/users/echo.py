from aiogram import types
from aiogram.types import ContentType, Message

from loader import dp


@dp.message_handler()
async def get_message(message: types.Message):
    """Answer for simple message"""
    await message.answer("I work with pictures only🤫")


