import io
import json

from aiogram.types import ContentType, Message, InputFile
from loader import dp, bot, db, _
from utils.misc import rate_limit

from PIL import Image
import pytesseract
import cv2
import requests
import easyocr


@rate_limit(limit=5)  #anti-spam
@dp.message_handler(content_types=ContentType.PHOTO)
async def getting_photo(message: Message):
    """Downloading to directory picture from message. Selecting background color from pic"""
    user_id = message.from_user.id
    url_api = "https://api.ocr.space/parse/image"

    try:
        await message.photo[-1].download('pictures/picture.png')
        photo_id = message.photo[-1].file_id
        await db.add_user_photo(user_id, photo_id)

        img = cv2.imread("pictures/picture.png")
        _, compressed_image = cv2.imencode('.png', img, [1, 90])
        file_bytes = io.BytesIO(compressed_image)

        result = requests.post(url_api,
                               files={'picture.png': file_bytes},
                               data={
                                   "apikey": 'K84303230088957',
                                   'language': 'rus'
                               })
        result = result.content.decode()
        result = json.loads(result)

        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        await message.answer(f'{text_detected}')
    except Exception as err:
        await message.answer(_(f'Oops, some unknown error\n{err}'))
