import io
import json
import os

import aiogram
import asyncpg
from aiogram.dispatcher import FSMContext, filters
from aiogram.types import ContentType, Message, InputFile, CallbackQuery
from loguru import logger

from keyboards.inline import photo_text_language_keyboard, check_subscription_keyboard
from keyboards.inline.callback_data import photo_text_language_callback
from loader import dp, bot, db, _
from utils.misc import rate_limit, check_subscription
import aiohttp

from data.config import OCR_API_KEY, CHANNEL
from PIL import Image
import pytesseract
import cv2
import requests
import easyocr
from datetime import datetime

URL_API = "https://api.ocr.space/parse/image"


async def get_api_response(photo_url, api_key, language: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL_API,
                                data={
                                    'url': photo_url,
                                    "apikey": api_key,
                                    'language': language,
                                    'detectOrientation': 'True',
                                    'filetype': ''
                                }) as response:
            return await response.text()


async def fetch_photo(url, photo_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(photo_path, 'wb') as file:
                file.write(data)


@rate_limit(limit=5)  #anti-spam
@dp.message_handler(filters.Regexp(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)'))
async def getting_url(message: Message, state: FSMContext):
    """Downloading to directory picture from message. Selecting background color from pic"""
    user_id = message.from_user.id
    is_chat_member = await check_subscription(user_id=user_id, channel=CHANNEL)

    if is_chat_member:
        user_subscribe = await db.checking_user_subscribe(user_id)

        if not user_subscribe:
            user_requests_per_day = await db.api_requests_per_day(user_id)

            if user_requests_per_day:
                try:
                    photo_link = message.text

                    try:
                        await db.add_user_photo(user_id, photo_link)
                        await message.answer(_('Choose the language of the text on the photo:'),
                                             reply_markup=photo_text_language_keyboard)

                        await state.set_state('ConfirmLangURLPhotoText')
                        await state.update_data(photo_link=photo_link)
                    except asyncpg.exceptions.UniqueViolationError:
                        photo_text = await db.get_photo(photo_link)

                        if photo_text:
                            await message.answer(photo_text)
                        else:
                            await message.answer(_('Choose the language of the text on the photo:'),
                                                 reply_markup=photo_text_language_keyboard)

                            await state.set_state('ConfirmLangURLPhotoText')
                            await state.update_data(photo_link=photo_link)
                except Exception as err:
                    logger.exception(f'{err}')
                    await message.answer(_('Oops, some unknown error'))
            else:
                await message.answer(_('You have reached your daily limit (5 photos/day)! Subscription needed!\n'
                                       'More information here -> /donate'))
        else:
            try:
                photo_link = message.text

                try:
                    await db.add_user_photo(user_id, photo_link)
                    await message.answer(_('Choose the language of the text on the photo:'),
                                         reply_markup=photo_text_language_keyboard)

                    await state.set_state('ConfirmLangURLPhotoText')
                    await state.update_data(photo_link=photo_link)
                except asyncpg.exceptions.UniqueViolationError:
                    photo_text = await db.get_photo(photo_link)

                    if photo_text:
                        await message.answer(photo_text)
                    else:
                        await message.answer(_('Choose the language of the text on the photo:'),
                                             reply_markup=photo_text_language_keyboard)

                        await state.set_state('ConfirmLangURLPhotoText')
                        await state.update_data(photo_link=photo_link)
            except Exception as err:
                logger.exception(f'{err}')
                await message.answer(_('Oops, some unknown error!'))
    else:
        await message.answer(_('⚠ OCR is available only for those who are subscribed to our channel!\n\n'
                             'Subscribe to <a href="https://t.me/TextFromImage">TEXT FROM IMAGE</a>, '
                             'use the buttons below ↡'),
                             reply_markup=check_subscription_keyboard,
                             disable_web_page_preview=True)


@dp.callback_query_handler(photo_text_language_callback.filter(), state='ConfirmLangURLPhotoText')
async def confirm_language_url_photo_text(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.edit_text(_('⏳ Wait a bit...'))

    user_id = call.from_user.id
    state_data = await state.get_data()
    photo_link = state_data.get('photo_link')
    photo_path = f'pictures/{call.from_user.id}.png'
    photo_lang = callback_data['language']

    if photo_lang == 'ukr':
        await fetch_photo(photo_link, photo_path)

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        picture = cv2.imread(photo_path, 0)
        text_from_photo = pytesseract.image_to_string(picture, lang='ukr', config='--oem 3 --psm 6')
        cv2.waitKey()

        if text_from_photo:
            await call.message.edit_text(f'{text_from_photo}')
            await db.add_photo_text(user_id=user_id, photo_id=photo_link, text=text_from_photo)
        else:
            await call.message.edit_text(_('There is no text on the photo!'))
            await db.add_photo_text(user_id=user_id, photo_id=photo_link, text=_('There is no text on the photo!'))
        pass
        os.remove(photo_path)
    else:
        try:
            response = json.loads(await get_api_response(photo_url=photo_link,
                                                         api_key=OCR_API_KEY, language=photo_lang))
            print(response)
            if '180 number of times within 3600 seconds' in response:
                await call.message.edit_text(_('Bot is overloaded now! Will be available within the hour\n'
                                               'Or sign up for a paid subscription - /donate'))
            else:
                is_error = bool(response.get("IsErroredOnProcessing"))

                if is_error:
                    error_message = response.get('ErrorMessage')[0]

                    if 'file size exceeds' in error_message.lower():
                        await call.message.edit_text(_('The photo size is too big! '
                                                     'Try to reduce the size of the photo or send another photo!\n'
                                                       'Or sign up for a paid subscription - /donate'))
                    elif 'timed out waiting' in error_message.lower():
                        await call.message.edit_text(_('Server overloaded, please try again later\n'
                                                       'Or sign up for a paid subscription - /donate'))
                    else:
                        print(error_message)
                        await call.message.edit_text(_('An unexpected error has occurred'))
                else:
                    text_from_photo = response.get("ParsedResults")[0].get("ParsedText")

                    if text_from_photo:
                        await call.message.edit_text(f'{text_from_photo}')
                        await db.add_photo_text(user_id=user_id, photo_id=photo_link, text=text_from_photo)
                    else:
                        await call.message.edit_text(_('There is no text on the photo!'))
                        await db.add_photo_text(user_id=user_id, photo_id=photo_link,
                                                text=_('There is no text on the photo!'))
        except Exception as err:
            print(err)
            await call.message.edit_text(_('An unexpected error has occurred'))
    await state.finish()
