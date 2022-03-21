import io
import json
import os

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, InputFile, CallbackQuery
from loguru import logger

from keyboards.inline import photo_text_language_keyboard
from keyboards.inline.callback_data import photo_text_language_callback
from loader import dp, bot, db, _
from utils.misc import rate_limit
import aiohttp

from data.config import OCR_API_KEY
from PIL import Image
import pytesseract
import cv2
import requests
import easyocr

URL_API = "https://api.ocr.space/parse/image"


async def get_transactions(url, photo_bytes, api_key, language: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                data={
                                    'picture.png': photo_bytes,
                                    "apikey": api_key,
                                    'language': language,
                                    'detectOrientation': 'True'
                                }) as response:
            return await response.text()


@rate_limit(limit=5)  #anti-spam
@dp.message_handler(content_types=ContentType.PHOTO)
async def getting_photo(message: Message, state: FSMContext):
    """Downloading to directory picture from message. Selecting background color from pic"""
    user_id = message.from_user.id
    url_api = "https://api.ocr.space/parse/image"

    try:
        photo_id = message.photo[-1].file_id
        photo_path = f'pictures/{photo_id[-5:]}.png'

        await message.photo[-1].download(photo_path)
        await db.add_user_photo(user_id, photo_id)

        await message.answer(_('Choose the language of the text on the photo:'),
                             reply_markup=photo_text_language_keyboard)

        await state.set_state('ConfirmLangPhotoText')
        await state.update_data(photo_path=photo_path)

    except Exception as err:
        logger.exception(f'{err}')
        await message.answer(_(f'Oops, some unknown error\n{err}'))


@dp.callback_query_handler(photo_text_language_callback.filter(), state='ConfirmLangPhotoText')
async def confirm_language_photo_text(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()

    state_data = await state.get_data()
    photo_path = state_data.get('photo_path')
    photo_lang = callback_data['language']

    photo = cv2.imread(photo_path)
    unused_var, compressed_image = cv2.imencode('.png', photo, [1, 90])
    photo_bytes = io.BytesIO(compressed_image)

    response = json.loads(await get_transactions(url=URL_API, photo_bytes=photo_bytes,
                                                 api_key=OCR_API_KEY, language=photo_lang))
    print(response)

    text_from_photo = response.get("ParsedResults")[0].get("ParsedText")

    if text_from_photo:
        await call.message.answer(f'{text_from_photo}')
    else:
        await call.message.answer(_('There is no text on the photo!'))

    # except aiogram.utils.exceptions.MessageTextIsEmpty:
    #     await call.message.answer(_('There is no text on the photo!'))

    os.remove(photo_path)

    await state.finish()