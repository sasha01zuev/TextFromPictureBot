from environs import Env
from pathlib import Path

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
ADMINS_ID = env.list("ADMINS_ID")
MAIN_ADMIN = env("MAIN_ADMIN")

PGUSER = env("PGUSER")
PGPASSWORD = env("PGPASSWORD")

IP = env("IP")

OCR_API_KEY = env("OCR_API_KEY")

I18N_DOMAIN = 'OCRbot'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'