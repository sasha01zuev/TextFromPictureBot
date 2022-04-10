from aiogram.types import InlineKeyboardButton
from loader import _


async def cancel_button():
    return InlineKeyboardButton(text=_("⬅ Cancel"), callback_data="cancel")
