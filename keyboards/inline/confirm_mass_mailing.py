from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

confirm_mass_mailing_keyboard = InlineKeyboardMarkup(row_width=1,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(text="✅ Подтвердить",
                                                                          callback_data="confirm_mass_mailing")
                                                 ],
                                                 [
                                                     InlineKeyboardButton(text="⬅ Отменить",
                                                                          callback_data="cancel_mass_mailing")
                                                 ]
                                             ])
