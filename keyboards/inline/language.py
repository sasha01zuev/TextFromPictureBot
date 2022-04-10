from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _
from keyboards.inline.cancel_button import cancel_button

language_keyboard = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text="🇺🇸 English",
                                                                     callback_data="en")
                                            ],
                                            [
                                                InlineKeyboardButton(text="🇷🇺 Русский",
                                                                     callback_data="ru")
                                            ],
                                            [
                                                InlineKeyboardButton(text="🇺🇦 Українська",
                                                                     callback_data="uk")
                                            ],
                                            [
                                                cancel_button
                                            ]


                                        ]
                                        )