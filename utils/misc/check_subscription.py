from aiogram import Bot


async def check_subscription(user_id, channel):
    """Checking if a user is a member of a group"""

    bot = Bot.get_current()
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()
