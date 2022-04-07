from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("help"))
async def _help(message: Message):
    """Command help"""

    await message.answer(_("Send me picture and I send text from it🖼💬\n"
                           "- Try to send precise image for more correct recognition✅\n"
                           "- If you got non correct text, \ntry to select another background️🔲↔🔳"))
