from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅ Cancel")
        ]
    ],
    resize_keyboard=True
)

cancel_mtu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅ Отмена")
        ]
    ],
    resize_keyboard=True
)