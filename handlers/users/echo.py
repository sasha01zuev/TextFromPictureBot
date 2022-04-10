from aiogram import types
from aiogram.types import ContentType, Message

from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler()
async def get_message(message: types.Message):
    """Receiving simple messages"""

    await message.answer(_("🤫 <b>I work with <a href='https://bit.ly/38DrV5Y'>photos</a> or "
                           "<a href='https://bit.ly/3rciXmB'>links</a> to the photo!</b>"),
                         disable_web_page_preview=True)


