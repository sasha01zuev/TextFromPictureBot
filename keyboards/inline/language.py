from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _
from keyboards.inline.cancel_button import cancel_button


async def language_keyboard():
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="🇺🇸 English",
                                                             callback_data="en")
                                    ],
                                    [
                                        InlineKeyboardButton(text="🏴‍☠ Харьковский, Одесский",
                                                             callback_data="ru")
                                    ],
                                    [
                                        InlineKeyboardButton(text="🇺🇦 Українська",
                                                             callback_data="uk")
                                    ],
                                    [
                                        await cancel_button()
                                    ]

                                ]
                                )
