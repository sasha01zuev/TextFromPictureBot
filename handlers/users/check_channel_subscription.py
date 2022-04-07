from aiogram.types import CallbackQuery

from data.config import CHANNEL
from loader import dp, _
from utils.misc import check_subscription


@dp.callback_query_handler(text="check_subscription")
async def check_subs(call: CallbackQuery):
    """Checking user subscribe to the bot channel"""

    user_id = call.from_user.id
    is_chat_member = await check_subscription(user_id=user_id, channel=CHANNEL)

    if is_chat_member:  # If user is subscribed to the bot channel
        await call.answer(text=_("✅ Confirmed"))
        await call.message.delete()
    else:
        await call.answer(text=_("❗ Not confirmed"))
