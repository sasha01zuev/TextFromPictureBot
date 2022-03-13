from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

message_type_keyboard = InlineKeyboardMarkup(row_width=1,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(text="❔ Question",
                                                                          callback_data="question")
                                                 ],
                                                 [
                                                     InlineKeyboardButton(text="🧩 Recommendation/Suggestion",
                                                                          callback_data="recommendation")
                                                 ],
                                                 [
                                                     InlineKeyboardButton(text="📊 Bug report",
                                                                          callback_data="bug_report")
                                                 ],
                                                 [
                                                     InlineKeyboardButton(text="📜 Other",
                                                                          callback_data="other")
                                                 ],
                                                 [
                                                     InlineKeyboardButton(text="⬅ Отменить",
                                                                          callback_data="cancel")
                                                 ]

                                             ])
