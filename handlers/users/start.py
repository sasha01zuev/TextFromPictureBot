from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("start"))
async def start(message: Message):
    await message.answer("Send me picture with text and I send you only text💬\n"
                         "I'll try to make it right😅")
