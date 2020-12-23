from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message
import cv2
import pytesseract
from PIL import Image
from loader import dp
from keyboards.inline import bg_color_keyboard


@dp.message_handler(content_types=ContentType.PHOTO)
async def getting_photo(message: Message):
    """Downloading to directory picture from message. Selecting background color from pic"""
    try:
        await message.photo[-1].download('pictures/picture.png')
        await message.answer("Choose background color:",  reply_markup=bg_color_keyboard)
    except Exception as err:
        await message.answer(f'Oops, some unknown error\n{err}')
