from aiogram.dispatcher.filters import Text, Command
from aiogram.types import Message

from keyboards.inline import message_type_keyboard
from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command('message_to_admin'))
async def message_to_admin(message: Message):
    """Message to admin via bot"""

    await message.answer(_("Select message type:"), reply_markup=message_type_keyboard)
