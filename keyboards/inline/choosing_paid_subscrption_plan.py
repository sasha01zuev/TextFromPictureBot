from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choosing_paid_subscription_plan_callback
from keyboards.inline.cancel_button import cancel_button
from loader import _


async def paid_subscription_plan_keyboard():
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("3$/month"),
                                     callback_data=choosing_paid_subscription_plan_callback.new(
                                         amount='3'))
            ],
            [
                InlineKeyboardButton(text=_("5$/month"),
                                     callback_data=choosing_paid_subscription_plan_callback.new(
                                         amount='5'))
            ],
            [
                await cancel_button()
            ]
        ]
    )
