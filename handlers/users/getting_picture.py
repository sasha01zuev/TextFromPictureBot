import asyncio
import io
import json
import os
import time

import aiogram
import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, InputFile, CallbackQuery
from loguru import logger

from keyboards.inline import photo_text_language_keyboard, check_subscription_keyboard
from keyboards.inline.callback_data import photo_text_language_callback
from loader import dp, bot, db, _
from utils.misc import rate_limit, check_subscription
import aiohttp

from data.config import OCR_API_KEY, OCR_URL_API, CHANNEL
from PIL import Image
import pytesseract
import cv2
import requests
import easyocr
from datetime import datetime
import concurrent.futures


async def get_api_response(photo_bytes, api_key, language: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=OCR_URL_API,
                                data={
                                    'picture.png': photo_bytes,
                                    "apikey": api_key,
                                    'language': language,
                                    'detectOrientation': 'True'
                                }) as response:
            return await response.text()


@rate_limit(limit=5)  # anti-spam
@dp.message_handler(content_types=ContentType.PHOTO)
async def getting_photo(message: Message, state: FSMContext):
    """Downloading to directory picture from message. Selecting background color from pic"""
    user_id = message.from_user.id
    is_chat_member = await check_subscription(user_id=user_id, channel=CHANNEL)

    if is_chat_member:
        user_subscribe = await db.checking_user_subscribe(user_id)

        if not user_subscribe:
            user_requests_per_day = await db.api_requests_per_day(user_id)

            if user_requests_per_day:
                try:
                    photo_id = message.photo[-1].file_id
                    print(photo_id)
                    photo_path = f'pictures/{photo_id[-5:]}.png'

                    await message.photo[-1].download(photo_path)

                    try:
                        await db.add_user_photo(user_id, photo_id)

                        await message.answer(_('Choose the language of the text on the photo:'),
                                             reply_markup=photo_text_language_keyboard)

                        await state.set_state('ConfirmLangPhotoText')
                        await state.update_data(photo_path=photo_path, photo_id=photo_id)
                    except asyncpg.exceptions.UniqueViolationError:
                        photo_text = await db.get_photo(photo_id)

                        if photo_text:
                            print(photo_text)
                            await message.answer(photo_text)
                            os.remove(photo_path)
                        else:
                            await message.answer(_('Choose the language of the text on the photo:'),
                                                 reply_markup=photo_text_language_keyboard)

                            await state.set_state('ConfirmLangPhotoText')
                            await state.update_data(photo_path=photo_path, photo_id=photo_id)

                except Exception as err:
                    await message.answer(_('Oops, some unknown error'))
            else:
                await message.answer(_('You have reached your daily limit (5 photos/day)! Subscription needed!\n'
                                       'More information here -> /donate'))
        else:
            try:
                photo_id = message.photo[-1].file_id
                print(photo_id)
                photo_path = f'pictures/{photo_id[-5:]}.png'

                await message.photo[-1].download(photo_path)

                try:
                    await db.add_user_photo(user_id, photo_id)

                    await message.answer(_('Choose the language of the text on the photo:'),
                                         reply_markup=photo_text_language_keyboard)

                    await state.set_state('ConfirmLangPhotoText')
                    await state.update_data(photo_path=photo_path, photo_id=photo_id)
                except asyncpg.exceptions.UniqueViolationError:
                    photo_text = await db.get_photo(photo_id)

                    if photo_text:
                        print(photo_text)
                        await message.answer(photo_text)
                        os.remove(photo_path)
                    else:
                        await message.answer(_('Choose the language of the text on the photo:'),
                                             reply_markup=photo_text_language_keyboard)

                        await state.set_state('ConfirmLangPhotoText')
                        await state.update_data(photo_path=photo_path, photo_id=photo_id)

            except Exception as err:
                await message.answer(_('Oops, some unknown error'))
    else:
        await message.answer(_('⚠ OCR is available only for those who are subscribed to our channel!\n\n'
                               'Subscribe to <a href="https://t.me/TextFromImage">TEXT FROM IMAGE</a>, '
                               'use the buttons below ↡'),
                             reply_markup=check_subscription_keyboard,
                             disable_web_page_preview=True)


@dp.callback_query_handler(photo_text_language_callback.filter(), state='ConfirmLangPhotoText')
async def confirm_language_photo_text(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.edit_text(_('⏳ Wait a bit...'))

    user_id = call.from_user.id
    state_data = await state.get_data()
    photo_path = state_data.get('photo_path')
    photo_id = state_data.get('photo_id')
    photo_lang = callback_data['language']

    if photo_lang == 'ukr':
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        picture = cv2.imread(photo_path, 0)
        text_from_photo = pytesseract.image_to_string(picture, lang='ukr', config='--oem 3 --psm 6')
        cv2.waitKey()

        if text_from_photo:
            await call.message.edit_text(f'{text_from_photo}')
            await db.add_photo_text(user_id=user_id, photo_id=photo_id, text=text_from_photo)
        else:
            await call.message.edit_text(_('There is no text on the photo!'))
            await db.add_photo_text(user_id=user_id, photo_id=photo_id, text=_('There is no text on the photo!'))
    else:
        try:
            photo = cv2.imread(photo_path)
            unused_var, compressed_image = cv2.imencode('.png', photo, [1, 90])
            photo_bytes = io.BytesIO(compressed_image)

            response = json.loads(await get_api_response(photo_bytes=photo_bytes,
                                                         api_key=OCR_API_KEY, language=photo_lang))

            if '180 number of times within 3600 seconds' in response:
                await call.message.edit_text(_('Bot is overloaded now! Will be available within the hour'
                                               'Or sign up for a paid subscription - /donate'))
            else:
                is_error = bool(response.get("IsErroredOnProcessing"))
                print(response)

                if is_error:
                    error_message = response.get('ErrorMessage')[0]
                    print(error_message)

                    if 'file size exceeds' in error_message.lower():
                        await call.message.edit_text(_('The photo size is too big! '
                                                     'Try to reduce the size of the photo or send another photo!'
                                                       'Or sign up for a paid subscription - /donate'))
                    elif 'timed out waiting' in error_message.lower():
                        await call.message.edit_text(_('Server overloaded, please try again later'
                                                       'Or sign up for a paid subscription - /donate'))
                else:
                    text_from_photo = response.get("ParsedResults")[0].get("ParsedText")

                    if text_from_photo:
                        await call.message.edit_text(f'{text_from_photo}')
                        await db.add_photo_text(user_id=user_id, photo_id=photo_id, text=text_from_photo)
                    else:
                        await call.message.edit_text(_('There is no text on the photo!'))
        except Exception as err:
            print(err)
            await call.message.edit_text(_('An unexpected error has occurred'))

    os.remove(photo_path)
    await state.finish()


@dp.callback_query_handler(text="check_subscription")
async def check_subs(call: CallbackQuery):
    user_id = call.from_user.id
    is_chat_member = await check_subscription(user_id=user_id, channel=CHANNEL)
    if is_chat_member:
        await call.answer(text=_("✅ Confirmed"))
        await call.message.delete()
    else:
        await call.answer(text=_("❗ Not confirmed"))
