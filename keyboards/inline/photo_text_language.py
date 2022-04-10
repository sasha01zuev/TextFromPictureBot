from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import photo_text_language_callback
from keyboards.inline.cancel_button import cancel_button


async def photo_text_language_keyboard():
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="English",
                                     callback_data=photo_text_language_callback.new(
                                         language="eng")),
                InlineKeyboardButton(text="Russian",
                                     callback_data=photo_text_language_callback.new(
                                         language="rus"))
            ],
            [
                InlineKeyboardButton(text="Ukrainian (Beta)",
                                     callback_data=photo_text_language_callback.new(
                                         language="ukr"))
            ],
            [
                InlineKeyboardButton(text="Arabic",
                                     callback_data=photo_text_language_callback.new(
                                         language="ara")),
                InlineKeyboardButton(text="Bulgarian",
                                     callback_data=photo_text_language_callback.new(
                                         language="bul"))
            ],
            [
                InlineKeyboardButton(text="Chinese (Simplified)",
                                     callback_data=photo_text_language_callback.new(
                                         language="chs")),
                InlineKeyboardButton(text="Chinese (Traditional",
                                     callback_data=photo_text_language_callback.new(
                                         language="cht"))
            ],
            [
                InlineKeyboardButton(text="Croatian",
                                     callback_data=photo_text_language_callback.new(
                                         language="hrv")),
                InlineKeyboardButton(text="Czech",
                                     callback_data=photo_text_language_callback.new(
                                         language="cze"))
            ],
            [
                InlineKeyboardButton(text="Danish",
                                     callback_data=photo_text_language_callback.new(
                                         language="dan")),
                InlineKeyboardButton(text="Dutch",
                                     callback_data=photo_text_language_callback.new(
                                         language="dut"))
            ],
            [
                InlineKeyboardButton(text="Finnish",
                                     callback_data=photo_text_language_callback.new(
                                         language="fin")),
                InlineKeyboardButton(text="French",
                                     callback_data=photo_text_language_callback.new(
                                         language="fre"))
            ],
            [
                InlineKeyboardButton(text="German",
                                     callback_data=photo_text_language_callback.new(
                                         language="ger")),
                InlineKeyboardButton(text="Greek",
                                     callback_data=photo_text_language_callback.new(
                                         language="gre"))
            ],
            [
                InlineKeyboardButton(text="Hungarian",
                                     callback_data=photo_text_language_callback.new(
                                         language="hun")),
                InlineKeyboardButton(text="Korean",
                                     callback_data=photo_text_language_callback.new(
                                         language="kor"))
            ],
            [
                InlineKeyboardButton(text="Italian",
                                     callback_data=photo_text_language_callback.new(
                                         language="ita")),
                InlineKeyboardButton(text="Japanese",
                                     callback_data=photo_text_language_callback.new(
                                         language="jpn"))
            ],
            [
                InlineKeyboardButton(text="Polish",
                                     callback_data=photo_text_language_callback.new(
                                         language="pol")),
                InlineKeyboardButton(text="Portuguese",
                                     callback_data=photo_text_language_callback.new(
                                         language="por"))
            ],
            [
                InlineKeyboardButton(text="Slovenian",
                                     callback_data=photo_text_language_callback.new(
                                         language="slv")),
                InlineKeyboardButton(text="Spanish",
                                     callback_data=photo_text_language_callback.new(
                                         language="spa"))
            ],
            [
                InlineKeyboardButton(text="Swedish",
                                     callback_data=photo_text_language_callback.new(
                                         language="swe")),
                InlineKeyboardButton(text="Turkish",
                                     callback_data=photo_text_language_callback.new(
                                         language="tur"))
            ],
            [
                await cancel_button()
            ]
        ]
    )
