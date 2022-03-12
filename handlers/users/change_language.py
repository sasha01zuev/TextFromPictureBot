from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, _
from utils.misc import rate_limit
from keyboards.inline import language_keyboard


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("language"))
async def change_language(message: Message):
    await message.answer(_('Choose your language:'), reply_markup=language_keyboard)