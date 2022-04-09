from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _

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
                                                InlineKeyboardButton(text=_("⬅ Отменить"),
                                                                     callback_data="cancel")
                                            ]

                                        ]
                                        )