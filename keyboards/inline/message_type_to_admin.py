from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _


async def message_type_keyboard():
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=_("❔ Question"),
                                                             callback_data="question")
                                    ],
                                    [
                                        InlineKeyboardButton(text=_("🧩 Recommendation/Suggestion"),
                                                             callback_data="recommendation")
                                    ],
                                    [
                                        InlineKeyboardButton(text=_("📊 Bug report"),
                                                             callback_data="bug_report")
                                    ],
                                    [
                                        InlineKeyboardButton(text=_("📜 Other"),
                                                             callback_data="other")
                                    ],
                                    [
                                        InlineKeyboardButton(text=_("⬅ Отменить"),
                                                             callback_data="cancel")
                                    ]

                                ])
