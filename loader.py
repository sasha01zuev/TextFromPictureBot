import asyncio
from loguru import logger

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.postgresql import Database
from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())

logger.add(f'info.log', format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}", rotation="10 MB",
           compression='zip', level="DEBUG", backtrace=True, diagnose=True)


