from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

donate_keyboard = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text="Support us",
                                                                    callback_data="donate_support")
                                           ],
                                           [
                                               InlineKeyboardButton(text="Paid subscription",
                                                                    callback_data="donate_paid_subscription")
                                           ]

                                       ]
                                       )
