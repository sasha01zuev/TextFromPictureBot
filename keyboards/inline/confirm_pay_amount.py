from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choosing_cryptocurrency_callback
from keyboards.inline.cancel_button import cancel_button
from loader import _


async def confirm_pay_amount_keyboard():
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("✅ Confirm"),
                                     callback_data='confirm_amount'),
                await cancel_button()
            ]

        ]
    )
