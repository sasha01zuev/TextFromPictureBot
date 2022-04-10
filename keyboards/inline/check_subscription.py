from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def check_subscription_keyboard():
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=_("[1] Subscribe"),
                                                             url="https://t.me/TextFromImage")
                                    ],
                                    [
                                        InlineKeyboardButton(text=_("[2] Check subscribe"),
                                                             callback_data="check_subscription")
                                    ]

                                ]
                                )
