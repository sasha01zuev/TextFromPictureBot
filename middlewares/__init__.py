from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware
from .checking_user_existence import CheckingUserExistence


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckingUserExistence())
