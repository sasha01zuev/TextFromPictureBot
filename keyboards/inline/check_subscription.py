from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_subscription_keyboard = InlineKeyboardMarkup(row_width=1,
                                                   inline_keyboard=[
                                                       [
                                                           InlineKeyboardButton(text="[1] Подписаться",
                                                                                url="https://t.me/TextFromImage")
                                                       ],
                                                       [
                                                           InlineKeyboardButton(text="[2] Проверить подписку",
                                                                                callback_data="check_subscription")
                                                       ]

                                                   ]
                                                   )
