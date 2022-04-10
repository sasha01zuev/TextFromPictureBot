from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.cancel_button import cancel_button
from loader import _


async def confirm_payment_keyboard(pay_url: str):
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("🔗 Pay"), url=pay_url)
            ],
            [
                InlineKeyboardButton(text=_("✅ Paid"),
                                     callback_data='confirm_payment'),
                await cancel_button()
            ]

        ]
    )
