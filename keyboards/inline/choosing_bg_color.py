from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import bg_color_callback

bg_color_keyboard = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(text="Light⚪",
                                                                      callback_data=bg_color_callback.new(
                                                                          color="light")),
                                                 InlineKeyboardButton(text="Dark⚫",
                                                                      callback_data=bg_color_callback.new(
                                                                          color="dark"))
                                             ]

                                         ]
                                         )
