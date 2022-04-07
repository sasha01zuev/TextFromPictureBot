from aiogram import types
from aiogram.types import ContentType, Message

from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler()
async def get_message(message: types.Message):
    """Receiving simple messages"""

    await message.answer(_("I work with pictures only🤫"))


