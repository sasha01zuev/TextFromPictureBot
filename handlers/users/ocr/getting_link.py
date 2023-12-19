import json
import json
import os

import aiohttp
import asyncpg
import cv2
import pytesseract

from aiogram.dispatcher import FSMContext, filters
from aiogram.types import Message, CallbackQuery
from loguru import logger

from data.config import OCR_API_KEY, OCR_URL_API, CHANNEL
from keyboards.inline import photo_text_language_keyboard, check_subscription_keyboard
from keyboards.inline.callback_data import photo_text_language_callback
from loader import dp, db, _
from utils.misc import rate_limit, check_subscription


async def get_api_response(photo_url, api_key, language: str):
    """Async function to get/post requests from/to HTTP or HTTPS"""

    async with aiohttp.ClientSession() as session:
        async with session.post(OCR_URL_API,
                                data={
                                    'url': photo_url,
                                    "apikey": api_key,
                                    'language': language,
                                    'detectOrientation': 'True',
                                    'filetype': ''
                                }) as response:
            return await response.text()


async def fetch_photo(url, photo_path):
    """Async function to download the photo"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(photo_path, 'wb') as file:
                file.write(data)


@rate_limit(limit=2)  # anti-spam
@dp.message_handler(filters.Regexp(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)'))
async def getting_url(message: Message, state: FSMContext):
    """Function accepts a link to photo from user"""

    user_id = message.from_user.id
    is_chat_member = await check_subscription(user_id=user_id, channel=CHANNEL)

    if is_chat_member:  # If user is subscribed to the bot channel
        user_subscribe = await db.checking_user_subscribe(user_id)

        if not user_subscribe:  # If user does not have a paid subscription
            user_requests_per_day = await db.api_requests_per_day(user_id)

            if user_requests_per_day:  # If user has not reached the request limit for the day
                try:
                    photo_link = message.text

                    try:  # If such link does not yet exist in the database
                        await db.add_user_photo(user_id, photo_link)
                        await message.answer(_('<b>Choose the language of the text on the photo:</b>'),
                                             reply_markup=await photo_text_language_keyboard())

                        await state.set_state('ConfirmLangURLPhotoText')
                        await state.update_data(photo_link=photo_link)
                        logger.info(f'{user_id} - Converting link\n'
                                    f'Paid subscription - False\n'
                                    f'photo_link - {photo_link}')
                    except asyncpg.exceptions.UniqueViolationError:  # If such link already exists
                        photo_text = await db.get_photo(photo_link)

                        if photo_text:  # If text of the photo exist in database
                            await message.answer(f'<code>{photo_text}</code>')
                            logger.success(f"{user_id} - Link photo converted (Link was in db)\n"
                                           f"Text - True\n"
                                           f"photo_link - {photo_link}\n"
                                           f"Paid subscription - False")
                        else:
                            await message.answer(_('<b>Choose the language of the text on the photo:</b>'),
                                                 reply_markup=await photo_text_language_keyboard())

                            await state.set_state('ConfirmLangURLPhotoText')
                            await state.update_data(photo_link=photo_link)
                            logger.info(f'{user_id} - Converting link\n'
                                        f'Paid subscription - False\n'
                                        f'photo_link - {photo_link}')
                except Exception as err:
                    await message.answer(_('😲 <b>Oops, some unknown error while getting the photo!</b>\n'))
                    logger.exception(f'{user_id} - Unknown error while getting link\n'
                                     f'Paid subscription - False\n'
                                     f'More details:\n{err}')
            else:
                await message.answer(_('❕<b>You have reached your daily limit (5 photos/day)! '
                                       'Subscription needed!</b>\n\n'
                                       '<b>More information here</b> → /donate'))
                logger.info(f'{user_id} - user has reached the request limit for the day')
        else:  # If user has a paid subscription
            try:
                photo_link = message.text

                try:  # If such link does not yet exist in the database
                    await db.add_user_photo(user_id, photo_link)
                    await message.answer(_('<b>Choose the language of the text on the photo:</b>'),
                                         reply_markup=await photo_text_language_keyboard())

                    await state.set_state('ConfirmLangURLPhotoText')
                    await state.update_data(photo_link=photo_link)
                    logger.info(f'{user_id} - Converting link\n'
                                f'Paid subscription - True\n'
                                f'photo_link - {photo_link}')
                except asyncpg.exceptions.UniqueViolationError:  # If such link already exists
                    photo_text = await db.get_photo(photo_link)

                    if photo_text:  # If text of the photo exist in database
                        await message.answer(f'<code>{photo_text}</code>')
                        logger.success(f"{user_id} - Link photo converted (Link was in db)\n"
                                       f"Text - True\n"
                                       f"photo_link - {photo_link}\n"
                                       f"Paid subscribe - True")
                    else:
                        await message.answer(_('<b>Choose the language of the text on the photo:</b>'),
                                             reply_markup=await photo_text_language_keyboard())

                        await state.set_state('ConfirmLangURLPhotoText')
                        await state.update_data(photo_link=photo_link)
                        logger.info(f'{user_id} - Converting link\n'
                                    f'Paid subscription - True\n'
                                    f'photo_link - {photo_link}')
            except Exception as err:
                await message.answer(_('😲 <b>Oops, some unknown error while getting the photo!</b>\n'))
                logger.exception(f'{user_id} - Unknown error while getting link\n'
                                 f'Paid subscription - True\n'
                                 f'More details:\n{err}')
    else:
        await message.answer(_('⚠ <b>OCR is available only for those who are subscribed to our channel!\n\n'
                               'Subscribe to <a href="https://t.me/TextFromPictureChannel">Text From Picture Channel</a>. '
                               'Use the buttons below</b> ↡'),
                             reply_markup=await check_subscription_keyboard(),
                             disable_web_page_preview=True)
        logger.info(f'{user_id} - user not subscribed to the bot channel')


@dp.callback_query_handler(photo_text_language_callback.filter(), state='ConfirmLangURLPhotoText')
async def confirm_language_url_photo_text(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Getting language from photo text and converting photo to text"""

    await call.answer(cache_time=5)
    await call.message.edit_text(_('⏳ Wait a bit...'))

    user_id = call.from_user.id
    state_data = await state.get_data()
    photo_link = state_data.get('photo_link')
    photo_path = f'pictures/{call.from_user.id}.png'
    photo_lang = callback_data['language']

    if photo_lang == 'ukr':  # If chosen Ukrainian language (this language is unavailable in API)
        await fetch_photo(photo_link, photo_path)

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # tesseract EXE
        picture = cv2.imread(photo_path, 0)  # Reading photo bytes from photo path
        text_from_photo = pytesseract.image_to_string(picture, lang='ukr', config='--oem 3 --psm 6')
        # Converting image to string
        cv2.waitKey()

        if text_from_photo:  # If the text in the picture was found
            await call.message.edit_text(f'<code>{text_from_photo}</code>')
            await db.add_photo_text(user_id=user_id, photo_id=photo_link, text=text_from_photo)
            logger.success(f"{user_id} - Link photo converted\n"
                           f"Text - True\n"
                           f"Language - {photo_lang}\n"
                           f"photo_link - {photo_link}\n")
        else:  # If text on the picture was not found
            await call.message.edit_text(_('❕<b>There is no text on the photo!</b>'))
            await db.add_photo_text(user_id=user_id, photo_id=photo_link, text=_('There is no text on the photo!'))
            logger.success(f"{user_id} - Link photo converted\n"
                           f"Text - False\n"
                           f"Language - {photo_lang}\n"
                           f"photo_link - {photo_link}\n")
        os.remove(photo_path)
    else:  # If one language is selected from the other 24
        try:
            response = json.loads(await get_api_response(photo_url=photo_link,
                                                         api_key=OCR_API_KEY, language=photo_lang))  # Getting response

            logger.debug(f'{user_id} - OCR_RESPONSE (LINK):\n'
                         f'{response}')

            if '180 number of times within 3600 seconds' in response:  # If more than 180 requests per hour
                await call.message.edit_text(_('⚠ <b>Bot is overloaded now! Will be available within the hour '
                                               'Or sign up for a paid subscription - /donate</b>'))
                logger.info(f'{user_id} - OCR_API exception: 180 requests per hour')
            else:
                is_error = bool(response.get("IsErroredOnProcessing"))

                if is_error:  # If error on processing of converting
                    error_message = response.get('ErrorMessage')[0]
                    logger.debug(f'{user_id} - OCR_API error (LINK):\n'
                                 f'Error message: {error_message}')

                    if 'file size exceeds' in error_message.lower():  # Big photo size error
                        await call.message.edit_text(_('⚠ <b>The photo size is too big! '
                                                       'Try to reduce the size of the photo or send another photo! '
                                                       'Or sign up for a paid subscription - /donate</b>'))
                    elif 'timed out waiting' in error_message.lower():  # Server overloading error
                        await call.message.edit_text(_('⚠ <b>Server overloaded, please try again later! '
                                                       'Or sign up for a paid subscription - /donate</b>'))
                    else:
                        await call.message.edit_text(_('⚠ <b>An unexpected error has occurred</b>'))
                else:
                    text_from_photo = response.get("ParsedResults")[0].get("ParsedText")

                    if text_from_photo:  # If text on the picture was found
                        await call.message.edit_text(f'<code>{text_from_photo}</code>')
                        await db.add_photo_text(user_id=user_id, photo_id=photo_link, text=text_from_photo)
                        logger.success(f"{user_id} - Link photo converted\n"
                                       f"Text - True\n"
                                       f"Language - {photo_lang}\n"
                                       f"photo_link - {photo_link}\n")
                    else:  # If text on the picture was not found
                        await call.message.edit_text(_('❕ <b>There is no text on the photo!</b>'))
                        await db.add_photo_text(user_id=user_id, photo_id=photo_link,
                                                text=_('There is no text on the photo!'))
                        logger.success(f"{user_id} - Link photo converted\n"
                                       f"Text - False\n"
                                       f"Language - {photo_lang}\n"
                                       f"photo_link - {photo_link}\n")
        except Exception as err:
            await call.message.edit_text(_('😲 <b>An unexpected error has occurred</b>'))
            logger.exception(f'{user_id} - Unknown error while getting OCR RESPONSE (LINK)\n'
                             f'More details:\n{err}')
    await state.finish()
