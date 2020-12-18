from loader import bot
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    import middlewares
    middlewares.setup(dp)
    await set_default_commands(dp)
    await on_startup_notify(dp)


async def on_shutdown(dp):
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
