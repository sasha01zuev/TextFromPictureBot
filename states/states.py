from aiogram.dispatcher.filters.state import StatesGroup, State

# Example:
# class Start(StatesGroup):
#     SetStartCommand = State()


class ConfirmMsgToAdmin(StatesGroup):
    SetMessageType = State()
