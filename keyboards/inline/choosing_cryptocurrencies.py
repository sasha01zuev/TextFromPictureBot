from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import choosing_cryptocurrency_callback
from keyboards.inline.cancel_button import cancel_button

choosing_cryptocurrencies_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="TON",
                                 callback_data=choosing_cryptocurrency_callback.new(
                                     currency='TON'
                                 ))
        ],
        [
            InlineKeyboardButton(text="USDT",
                                 callback_data=choosing_cryptocurrency_callback.new(
                                     currency='USDT'
                                 ))
        ],
        [
            InlineKeyboardButton(text="BUSD",
                                 callback_data=choosing_cryptocurrency_callback.new(
                                     currency='BUSD'
                                 ))
        ],
        [
            InlineKeyboardButton(text="BNB",
                                 callback_data=choosing_cryptocurrency_callback.new(
                                     currency='BNB'
                                 ))
        ],
        [
            cancel_button
        ]

    ]
)
