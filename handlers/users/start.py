from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, db, _
from utils.misc import rate_limit
from keyboards.inline.language import language_keyboard


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("start"))
async def start(message: Message):
    """Registration a new user in database"""

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    user = await db.get_user(user_id)

    if not user:  # If user is already registered
        if message.from_user.language_code in ['ru', 'be', 'ky', 'kk', 'tg', 'uz']:
            lang_code = 'ru'
        elif message.from_user.language_code == 'uk':
            lang_code = 'uk'
        else:
            lang_code = 'en'

        await db.add_user(user_id, username, first_name)
        await db.add_user_info(user_id, lang_code)
        await message.answer(_("Hi, {first_name}😃\n\n"
                               "I can convert <u>photo to text</u>📝\n"
                               "Send me <b>photo</b> or <b>URL to photo</b> with text "
                               "and I will try to make it right🗯").format(first_name=first_name))

        await message.answer(_('<b>Choose your language:</b>'), reply_markup=await language_keyboard())
    else:
        await message.answer(_('You have already been registered!'))
