from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware


class ACLMiddleware(I18nMiddleware):
    """International middleware"""

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        from loader import db
        user = types.User.get_current()
        user_language = await db.get_user_language(user.id)

        if user_language:
            return user_language
        else:
            if user.language_code in ['ru', 'be', 'ky', 'kk', 'tg', 'uz']:
                return 'ru'
            elif user.language_code == 'uk':
                return 'uk'
            else:
                return 'en'
