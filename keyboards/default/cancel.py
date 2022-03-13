from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅ Cancel")
        ]
    ],
    resize_keyboard=True
)