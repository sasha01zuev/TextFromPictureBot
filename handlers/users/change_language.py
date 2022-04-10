from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.inline import language_keyboard
from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("language"))
async def change_language(message: Message):
    """Command change language"""

    await message.answer(_('<b>Choose your language:</b>'), reply_markup=await language_keyboard())
