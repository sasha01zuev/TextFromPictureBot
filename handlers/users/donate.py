from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.inline import donate_keyboard
from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=2)  # Anti-spam
@dp.message_handler(Command("donate"))
async def donate(message: Message):
    """Command donate"""

    await message.answer(_('To support us or get a paid subscription, you need to register in the official telegram '
                           'crypto wallet bot - @CryptoBot and top up your wallet\n\n'
                           '- If you chose "support us" -- you can choose any amount to donate\n\n'
                           '- If you have chosen "paid subscription" -- you can choose several types of subscription:\n'
                           '    · 30$/month - 3000 photos/hour, 125.000 photos/month, photo size limit - 5MB, '
                           'more servers - less load\n'
                           '    · 60$/month - 6000 photos/hour, 250.000 photos/month, photo size limit - 100MB, '
                           'more servers - less load'), reply_markup=donate_keyboard)
