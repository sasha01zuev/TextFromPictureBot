from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("help"))
async def start(message: Message):
    await message.answer("Send me picture and I send text from it🖼💬\n"
                         "- Try to send precise image for more correct recognition✅\n"
                         "- If you got uncorrect text, \ntry to select another background️🔲↔🔳")
