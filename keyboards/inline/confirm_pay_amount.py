from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choosing_cryptocurrency_callback
from keyboards.inline.cancel_button import cancel_button
from loader import _

confirm_pay_amount_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("✅ Confirm"),
                                 callback_data='confirm_amount'),
            cancel_button
        ]

    ]
)
