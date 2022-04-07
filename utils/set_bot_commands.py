from aiogram import types


async def set_default_commands(dp):
    """Set default commands for users"""

    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start Bot"),
        types.BotCommand("help", 'Help/Instruction')
    ])
