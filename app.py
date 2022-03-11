from loader import bot
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    import middlewares
    middlewares.setup(dp)
    await set_default_commands(dp)
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
