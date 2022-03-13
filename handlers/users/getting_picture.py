from aiogram.types import ContentType, Message
from loader import dp, bot, db, _
from utils.misc import rate_limit


@rate_limit(limit=5)  #anti-spam
@dp.message_handler(content_types=ContentType.PHOTO)
async def getting_photo(message: Message):
    """Downloading to directory picture from message. Selecting background color from pic"""
    user_id = message.from_user.id

    try:
        await message.photo[-1].download('pictures/picture.png')
        photo_id = message.photo[-1].file_id
        await db.add_user_photo(user_id, photo_id)
        # await message.answer("Choose background color:",  reply_markup=bg_color_keyboard)
    except Exception as err:
        await message.answer(_(f'Oops, some unknown error\n{err}'))
