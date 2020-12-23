import cv2
import pytesseract
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import language_callback
from loader import dp


@dp.callback_query_handler(language_callback.filter(lang='l_eng'))
async def extracting_text(call: CallbackQuery):
    """Extracting text from picture"""
    await call.answer(cache_time=5)
    await call.message.delete()

    picture = 'pictures/picture.png'
    picture = cv2.imread(picture, 0)

    output_text = pytesseract.image_to_string(picture, lang='eng', config='--oem 3 --psm 6')

    await call.message.answer(output_text)
    cv2.waitKey()
