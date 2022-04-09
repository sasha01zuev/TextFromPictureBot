from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("contacts"))
async def contacts(message: Message):
    """Command help"""

    await message.answer(_("<b>CONTACTS:\n\n"
                           "👨‍💻 Chief Administrator: @Sasha_Zuev\n\n"
                           "💬 All updates and all news will be in our channel: t.me/TextFromImage\n\n"
                           "👥 Our chat: t.me/TextFromImageChat</b>"))