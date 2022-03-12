from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware
from .checking_user_existence import CheckingUserExistence
from .blacklist import SetBlacklist
from .language import ACLMiddleware
from data.config import I18N_DOMAIN, LOCALES_DIR


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckingUserExistence())
    dp.middleware.setup(SetBlacklist())


def setup_language(dp: Dispatcher):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
