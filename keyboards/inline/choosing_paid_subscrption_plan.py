from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choosing_paid_subscription_plan_callback
from keyboards.inline.cancel_button import cancel_button

paid_subscription_plan_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="30$/month",
                                 callback_data=choosing_paid_subscription_plan_callback.new(
                                     amount='30'))
        ],
        [
            InlineKeyboardButton(text="60$/month",
                                 callback_data=choosing_paid_subscription_plan_callback.new(
                                     amount='60'))
        ]
    ]
)
