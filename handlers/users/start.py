from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, db, _
from utils.misc import rate_limit
from keyboards.inline import language_keyboard


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("start"))
async def start(message: Message):
    """Registration a new user in database"""

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    user = await db.get_user(user_id)

    if not user:  # If user is already registered
        await db.add_user(user_id, username, first_name)
        await db.add_user_info(user_id)
        await message.answer(_("Send me picture with text and I send you only text💬\n"
                             "I'll try to make it right😅"))

        await message.answer(_('Choose your language:'), reply_markup=language_keyboard)
    else:
        await message.answer(_('You have already been registered!'))
