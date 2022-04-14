from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, _
from utils.misc import rate_limit
from data.config import CHAT


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("help"))
async def _help(message: Message):
    """Command help"""

    await message.answer(_("<b>It's a bot for fetching text from photos.</b>\n\n"
                           "🔗 Send me link to photo which ends with .png .jpg .gif\n"
                           "<b>For example:</b> <code>https://.../picture.png</code>\n\n"
                           "🖼 Send me photo. Only one photo - I can't fetch text from photo-albums yet\n\n"
                           "👆 Just tap on the text to copy it to clipboard 📋\n\n"
                           "If you have any questions or problems, then write to our chat - {chat} "
                           "or our admins - /message_to_admin").format(chat=CHAT))
