from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import language_callback

"""   
'd' and 'l' before keyboard name is d - 'dark' a - 'light'   
"""
d_language_keyboard = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="English🇺🇸 ",
                                                                        callback_data=language_callback.new(
                                                                            lang="d_eng")),
                                                   InlineKeyboardButton(text="Русский🇷🇺",
                                                                        callback_data=language_callback.new(
                                                                            lang="d_rus")),
                                                   InlineKeyboardButton(text="Український🇺🇦",
                                                                        callback_data=language_callback.new(
                                                                            lang="d_ukr"))
                                               ],
                                               [
                                                   InlineKeyboardButton(text="All in one🇺🇳",
                                                                        callback_data=language_callback.new(
                                                                            lang="d_all"))
                                               ]


                                           ]
                                           )

l_language_keyboard = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="English🇺🇸 ",
                                                                        callback_data=language_callback.new(
                                                                            lang="l_eng")),
                                                   InlineKeyboardButton(text="Русский🇷🇺",
                                                                        callback_data=language_callback.new(
                                                                            lang="l_rus")),
                                                   InlineKeyboardButton(text="Український🇺🇦",
                                                                        callback_data=language_callback.new(
                                                                            lang="l_ukr"))
                                               ],
                                               [
                                                   InlineKeyboardButton(text="All in one🇺🇳",
                                                                        callback_data=language_callback.new(
                                                                            lang="l_all"))
                                               ]

                                           ]
                                           )
