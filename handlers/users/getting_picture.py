from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message
import cv2
import pytesseract
from loader import dp


@dp.message_handler(content_types=ContentType.PHOTO)
async def getting_photo(message: Message):
    """Getting and downloading to directory photo from message"""

    await message.answer("Скачал фото! 🤨😲")
    picture_id = message.photo[-1].file_id
    await message.photo[-1].download('pictures/picture.jpg')
    print(picture_id)