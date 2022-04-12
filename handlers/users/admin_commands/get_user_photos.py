from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from data.config import ADMINS_ID

from loader import dp, db, bot


@dp.message_handler(Command('get_user_photos'), user_id=ADMINS_ID)
async def get_user_photos(message: Message):
    try:
        user_id, photos_quantity = message.get_args().split()

        if 0 < int(photos_quantity) < 100:
            user_photos = await db.get_user_photos(int(user_id), limit=int(photos_quantity))
            if user_photos:
                for photo in user_photos:
                    photo_id = photo['photo_id']
                    try:
                        await message.answer_photo(photo_id)
                    except:
                        await message.answer(photo_id)
            else:
                await message.answer('Фото нету!')
        else:
            await message.answer('Количество фотографий 0-100!')
    except Exception as err:
        await message.answer(f'Ошибка!\n'
                             f'Следуйте шаблону: /get_user_photos [user_id] [photos_quantity]\n'
                             f'Подробнее:\n{err}')
