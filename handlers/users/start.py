from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, db
from utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    await db.add_user(user_id, username, first_name)
    await db.add_user_info(user_id)
    await message.answer("Send me picture with text and I send you only text💬\n"
                         "I'll try to make it right😅")
