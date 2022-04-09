from aiogram import types


async def set_default_commands(dp):
    """Set default commands for users"""

    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start Bot"),
        types.BotCommand("language", "Change bot language"),
        types.BotCommand("donate", "Sign up for a paid subscription or donate"),
        types.BotCommand("help", 'How to use this bot'),
        types.BotCommand("contacts", 'Our contacts and links'),

    ])
