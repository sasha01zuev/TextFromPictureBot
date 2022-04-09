from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _

donate_keyboard = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text=_("Support us"),
                                                                    callback_data="donate_support")
                                           ],
                                           [
                                               InlineKeyboardButton(text=_("Paid subscription"),
                                                                    callback_data="donate_paid_subscription")
                                           ]

                                       ]
                                       )
